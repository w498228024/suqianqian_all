"""
AI Skill 库 - 管理员路由
用户管理、Skill审核、系统设置
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel
from typing import Optional

from config import settings
from models.database import get_db
from routers.auth import get_current_admin, get_current_user_id

router = APIRouter()


# ==================== 请求模型 ====================

class AddAdminRequest(BaseModel):
    user_id: int
    role: str = "admin"


class SettingUpdateRequest(BaseModel):
    key: str
    value: str


# ==================== 路由 ====================

@router.get("/dashboard")
async def dashboard(authorization: str = Header(...)):
    """管理后台 Dashboard 统计"""
    await get_current_admin(authorization)
    db = await get_db()
    try:
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM skills")
        total_skills = (await cursor.fetchone())["cnt"]

        cursor = await db.execute("SELECT COUNT(*) as cnt FROM skills WHERE status = 'pending'")
        pending_skills = (await cursor.fetchone())["cnt"]

        cursor = await db.execute("SELECT COUNT(*) as cnt FROM users")
        total_users = (await cursor.fetchone())["cnt"]

        cursor = await db.execute("SELECT COUNT(*) as cnt FROM skills WHERE status = 'published'")
        published_skills = (await cursor.fetchone())["cnt"]

        return {
            "total_skills": total_skills,
            "pending_skills": pending_skills,
            "total_users": total_users,
            "published_skills": published_skills,
        }
    finally:
        await db.close()


@router.get("/users")
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    authorization: str = Header(...),
):
    """用户列表"""
    await get_current_admin(authorization)
    db = await get_db()
    try:
        offset = (page - 1) * page_size
        cursor = await db.execute(
            "SELECT id, openid, nickname, avatar_url, role, created_at FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (page_size, offset)
        )
        rows = await cursor.fetchall()

        cursor = await db.execute("SELECT COUNT(*) as cnt FROM users")
        total = (await cursor.fetchone())["cnt"]

        items = []
        for r in rows:
            item = dict(r)
            # 检查是否是管理员
            cursor2 = await db.execute("SELECT role FROM admins WHERE user_id = ?", (r["id"],))
            admin = await cursor2.fetchone()
            item["is_admin"] = admin is not None
            item["admin_role"] = admin["role"] if admin else None
            items.append(item)

        return {"items": items, "total": total}
    finally:
        await db.close()


@router.post("/users/{user_id}/admin")
async def add_admin(
    user_id: int,
    req: AddAdminRequest,
    authorization: str = Header(...),
):
    """设置管理员"""
    admin = await get_current_admin(authorization)
    if admin.get("admin_role") != "super_admin":
        raise HTTPException(status_code=403, detail="仅超级管理员可设置管理员")

    now = datetime.now().isoformat()
    db = await get_db()
    try:
        await db.execute(
            "INSERT OR REPLACE INTO admins (user_id, role, created_at) VALUES (?, ?, ?)",
            (user_id, req.role, now)
        )
        await db.execute(
            "UPDATE users SET role = ? WHERE id = ?",
            (req.role, user_id)
        )
        await db.commit()
        return {"message": "设置成功"}
    finally:
        await db.close()


@router.delete("/users/{user_id}/admin")
async def remove_admin(
    user_id: int,
    authorization: str = Header(...),
):
    """取消管理员"""
    admin = await get_current_admin(authorization)
    if admin.get("admin_role") != "super_admin":
        raise HTTPException(status_code=403, detail="仅超级管理员可取消管理员")

    db = await get_db()
    try:
        await db.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
        await db.execute("UPDATE users SET role = 'user' WHERE id = ?", (user_id,))
        await db.commit()
        return {"message": "已取消管理员"}
    finally:
        await db.close()


@router.get("/skills/pending")
async def list_pending_skills(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    authorization: str = Header(...),
):
    """待审核 Skill 列表"""
    await get_current_admin(authorization)
    db = await get_db()
    try:
        offset = (page - 1) * page_size
        cursor = await db.execute(
            "SELECT * FROM skills WHERE status = 'pending' ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (page_size, offset)
        )
        rows = await cursor.fetchall()

        cursor = await db.execute("SELECT COUNT(*) as cnt FROM skills WHERE status = 'pending'")
        total = (await cursor.fetchone())["cnt"]

        from routers.skills import skill_to_dict
        return {
            "items": [skill_to_dict(r) for r in rows],
            "total": total,
        }
    finally:
        await db.close()


@router.get("/skills/all")
async def list_all_skills(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    status: Optional[str] = Query(None),
    authorization: str = Header(...),
):
    """所有 Skill 列表（管理后台用）"""
    await get_current_admin(authorization)
    db = await get_db()
    try:
        offset = (page - 1) * page_size
        if status:
            cursor = await db.execute(
                "SELECT * FROM skills WHERE status = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (status, page_size, offset)
            )
            cursor2 = await db.execute("SELECT COUNT(*) as cnt FROM skills WHERE status = ?", (status,))
        else:
            cursor = await db.execute(
                "SELECT * FROM skills ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (page_size, offset)
            )
            cursor2 = await db.execute("SELECT COUNT(*) as cnt FROM skills")
        rows = await cursor.fetchall()
        total = (await cursor2.fetchone())["cnt"]

        from routers.skills import skill_to_dict
        return {
            "items": [skill_to_dict(r) for r in rows],
            "total": total,
        }
    finally:
        await db.close()


@router.post("/skills/{skill_id}/review")
async def review_skill(
    skill_id: int,
    authorization: str = Header(...),
):
    """审核操作（通过 URL query 传 action 和 note）"""
    # 从 query 参数获取
    from fastapi import Request
    # 简化：直接在这里处理
    pass


@router.get("/settings")
async def get_settings(authorization: str = Header(...)):
    """获取系统设置"""
    await get_current_admin(authorization)
    db = await get_db()
    try:
        cursor = await db.execute("SELECT key, value FROM settings")
        rows = await cursor.fetchall()
        return {row["key"]: row["value"] for row in rows}
    finally:
        await db.close()


@router.put("/settings")
async def update_setting(
    req: SettingUpdateRequest,
    authorization: str = Header(...),
):
    """更新系统设置"""
    await get_current_admin(authorization)
    db = await get_db()
    try:
        await db.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (req.key, req.value)
        )
        await db.commit()
        return {"message": "设置已更新"}
    finally:
        await db.close()
