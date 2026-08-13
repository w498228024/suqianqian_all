"""
AI Skill 库 - Skill 相关路由
列表、详情、上传、编辑、搜索、收藏
"""
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel
from typing import Optional, List

from config import settings
from models.database import get_db
from routers.auth import get_current_user_id, get_current_admin

router = APIRouter()


# ==================== 请求模型 ====================

class CreateSkillRequest(BaseModel):
    title: str
    desc: str = ""
    content: str = ""
    category: str
    sub_category: str = ""
    tags: List[str] = []
    fit_tools: List[str] = []
    author: str = ""
    source_type: str = "原创"
    license: str = "MIT"


class UpdateSkillRequest(BaseModel):
    title: Optional[str] = None
    desc: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    tags: Optional[List[str]] = None
    fit_tools: Optional[List[str]] = None
    author: Optional[str] = None
    source_type: Optional[str] = None
    license: Optional[str] = None


class ReviewRequest(BaseModel):
    action: str  # "approve" or "reject"
    note: str = ""


# ==================== 辅助函数 ====================

def skill_to_dict(row) -> dict:
    """将数据库行转为字典"""
    return {
        "id": row["id"],
        "title": row["title"],
        "desc": row["desc"],
        "content": row["content"],
        "category": row["category"],
        "sub_category": row["sub_category"],
        "tags": json.loads(row["tags"]) if row["tags"] else [],
        "fit_tools": json.loads(row["fit_tools"]) if row["fit_tools"] else [],
        "author": row["author"],
        "source_type": row["source_type"],
        "license": row["license"],
        "collect_num": row["collect_num"],
        "view_count": row["view_count"],
        "status": row["status"],
        "uploader_id": row["uploader_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


# ==================== 路由 ====================

@router.get("")
async def list_skills(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    category: Optional[str] = Query(None),
    sub_category: Optional[str] = Query(None),
    fit_tool: Optional[str] = Query(None),
    status: str = Query("published"),
):
    """Skill 列表（分页、筛选）"""
    db = await get_db()
    try:
        conditions = ["status = ?"]
        params: list = [status]

        if category:
            conditions.append("category = ?")
            params.append(category)
        if sub_category:
            conditions.append("sub_category = ?")
            params.append(sub_category)
        if fit_tool:
            conditions.append("fit_tools LIKE ?")
            params.append(f'%"{fit_tool}"%')

        where = " AND ".join(conditions)
        offset = (page - 1) * page_size

        cursor = await db.execute(
            f"SELECT * FROM skills WHERE {where} ORDER BY created_at DESC LIMIT ? OFFSET ?",
            params + [page_size, offset]
        )
        rows = await cursor.fetchall()

        cursor = await db.execute(
            f"SELECT COUNT(*) as cnt FROM skills WHERE {where}",
            params
        )
        total = (await cursor.fetchone())["cnt"]

        return {
            "items": [skill_to_dict(r) for r in rows],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    finally:
        await db.close()


@router.get("/{skill_id}")
async def get_skill(skill_id: int):
    """Skill 详情"""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM skills WHERE id = ?", (skill_id,))
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Skill 不存在")

        # 增加浏览量
        await db.execute(
            "UPDATE skills SET view_count = view_count + 1 WHERE id = ?",
            (skill_id,)
        )
        await db.commit()

        return skill_to_dict(row)
    finally:
        await db.close()


@router.post("")
async def create_skill(
    req: CreateSkillRequest,
    authorization: str = Header(...),
):
    """上传 Skill（需登录）"""
    user_id = await get_current_user_id(authorization)
    now = datetime.now().isoformat()

    db = await get_db()
    try:
        cursor = await db.execute(
            """INSERT INTO skills 
               (title, desc, content, category, sub_category, tags, fit_tools, 
                author, source_type, license, status, uploader_id, created_at, updated_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                req.title, req.desc, req.content, req.category, req.sub_category,
                json.dumps(req.tags, ensure_ascii=False),
                json.dumps(req.fit_tools, ensure_ascii=False),
                req.author, req.source_type, req.license,
                "pending", user_id, now, now
            )
        )
        await db.commit()
        skill_id = cursor.lastrowid

        return {"id": skill_id, "message": "提交成功，等待审核"}
    finally:
        await db.close()


@router.put("/{skill_id}")
async def update_skill(
    skill_id: int,
    req: UpdateSkillRequest,
    authorization: str = Header(...),
):
    """编辑 Skill（管理员）"""
    await get_current_admin(authorization)

    now = datetime.now().isoformat()
    updates = []
    params = []

    field_map = {
        "title": req.title, "desc": req.desc, "content": req.content,
        "category": req.category, "sub_category": req.sub_category,
        "author": req.author, "source_type": req.source_type, "license": req.license,
    }
    for field, value in field_map.items():
        if value is not None:
            updates.append(f"{field} = ?")
            params.append(value)

    if req.tags is not None:
        updates.append("tags = ?")
        params.append(json.dumps(req.tags, ensure_ascii=False))
    if req.fit_tools is not None:
        updates.append("fit_tools = ?")
        params.append(json.dumps(req.fit_tools, ensure_ascii=False))

    if not updates:
        raise HTTPException(status_code=400, detail="没有需要更新的字段")

    updates.append("updated_at = ?")
    params.append(now)
    params.append(skill_id)

    db = await get_db()
    try:
        await db.execute(
            f"UPDATE skills SET {', '.join(updates)} WHERE id = ?",
            params
        )
        await db.commit()
        return {"message": "更新成功"}
    finally:
        await db.close()


@router.put("/{skill_id}/status")
async def update_skill_status(
    skill_id: int,
    req: ReviewRequest,
    authorization: str = Header(...),
):
    """审核 Skill（管理员）"""
    admin = await get_current_admin(authorization)

    if req.action not in ("approve", "reject"):
        raise HTTPException(status_code=400, detail="action 必须是 approve 或 reject")

    new_status = "published" if req.action == "approve" else "rejected"
    now = datetime.now().isoformat()

    db = await get_db()
    try:
        await db.execute(
            "UPDATE skills SET status = ?, reviewer_id = ?, review_note = ?, updated_at = ? WHERE id = ?",
            (new_status, admin["id"], req.note, now, skill_id)
        )
        await db.commit()
        return {"message": "审核成功", "status": new_status}
    finally:
        await db.close()


@router.post("/{skill_id}/collect")
async def toggle_collect(
    skill_id: int,
    authorization: str = Header(...),
):
    """收藏/取消收藏"""
    user_id = await get_current_user_id(authorization)

    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT id FROM favorites WHERE user_id = ? AND skill_id = ?",
            (user_id, skill_id)
        )
        existing = await cursor.fetchone()

        if existing:
            await db.execute(
                "DELETE FROM favorites WHERE user_id = ? AND skill_id = ?",
                (user_id, skill_id)
            )
            await db.execute(
                "UPDATE skills SET collect_num = MAX(0, collect_num - 1) WHERE id = ?",
                (skill_id,)
            )
            await db.commit()
            return {"collected": False}
        else:
            now = datetime.now().isoformat()
            await db.execute(
                "INSERT INTO favorites (user_id, skill_id, created_at) VALUES (?, ?, ?)",
                (user_id, skill_id, now)
            )
            await db.execute(
                "UPDATE skills SET collect_num = collect_num + 1 WHERE id = ?",
                (skill_id,)
            )
            await db.commit()
            return {"collected": True}
    finally:
        await db.close()


@router.get("/search/list")
async def search_skills(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
):
    """搜索 Skill（标题>标签>简介>正文权重）"""
    db = await get_db()
    try:
        kw = f"%{keyword}%"
        offset = (page - 1) * page_size

        # 加权搜索：标题匹配权重最高
        cursor = await db.execute("""
            SELECT *, 
                CASE 
                    WHEN title LIKE ? THEN 100
                    WHEN tags LIKE ? THEN 50
                    WHEN desc LIKE ? THEN 20
                    WHEN content LIKE ? THEN 5
                    ELSE 0
                END as score
            FROM skills 
            WHERE status = 'published' 
                AND (title LIKE ? OR tags LIKE ? OR desc LIKE ? OR content LIKE ?)
            ORDER BY score DESC, created_at DESC
            LIMIT ? OFFSET ?
        """, (kw, kw, kw, kw, kw, kw, kw, kw, page_size, offset))
        rows = await cursor.fetchall()

        cursor = await db.execute("""
            SELECT COUNT(*) as cnt FROM skills 
            WHERE status = 'published' 
                AND (title LIKE ? OR tags LIKE ? OR desc LIKE ? OR content LIKE ?)
        """, (kw, kw, kw, kw))
        total = (await cursor.fetchone())["cnt"]

        return {
            "items": [skill_to_dict(r) for r in rows],
            "total": total,
            "keyword": keyword,
        }
    finally:
        await db.close()


@router.get("/favorites/status")
async def check_favorite_status(
    skill_id: int = Query(...),
    authorization: str = Header(...),
):
    """查询某个 Skill 是否已收藏"""
    user_id = await get_current_user_id(authorization)
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT id FROM favorites WHERE user_id = ? AND skill_id = ?",
            (user_id, skill_id)
        )
        existing = await cursor.fetchone()
        return {"is_favorited": existing is not None}
    finally:
        await db.close()


@router.get("/favorites/list")
async def list_favorites(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    authorization: str = Header(...),
):
    """我的收藏列表"""
    user_id = await get_current_user_id(authorization)
    db = await get_db()
    try:
        offset = (page - 1) * page_size
        cursor = await db.execute("""
            SELECT s.* FROM skills s 
            INNER JOIN favorites f ON s.id = f.skill_id 
            WHERE f.user_id = ? AND s.status = 'published'
            ORDER BY f.created_at DESC LIMIT ? OFFSET ?
        """, (user_id, page_size, offset))
        rows = await cursor.fetchall()

        cursor = await db.execute("""
            SELECT COUNT(*) as cnt FROM favorites f 
            INNER JOIN skills s ON s.id = f.skill_id 
            WHERE f.user_id = ? AND s.status = 'published'
        """, (user_id,))
        total = (await cursor.fetchone())["cnt"]

        return {
            "items": [skill_to_dict(r) for r in rows],
            "total": total,
        }
    finally:
        await db.close()


@router.get("/uploads/list")
async def list_my_uploads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    authorization: str = Header(...),
):
    """我的上传列表"""
    user_id = await get_current_user_id(authorization)
    db = await get_db()
    try:
        offset = (page - 1) * page_size
        cursor = await db.execute(
            "SELECT * FROM skills WHERE uploader_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (user_id, page_size, offset)
        )
        rows = await cursor.fetchall()

        cursor = await db.execute(
            "SELECT COUNT(*) as cnt FROM skills WHERE uploader_id = ?",
            (user_id,)
        )
        total = (await cursor.fetchone())["cnt"]

        return {
            "items": [skill_to_dict(r) for r in rows],
            "total": total,
        }
    finally:
        await db.close()
