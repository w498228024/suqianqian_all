"""
AI Skill 库 - 认证路由
微信登录 + 管理员密码登录
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

from config import settings
from models.database import get_db
from services.wechat_service import code2session

router = APIRouter()


# ==================== 请求模型 ====================

class WechatLoginRequest(BaseModel):
    code: str


class AdminLoginRequest(BaseModel):
    password: str


# ==================== JWT 工具函数 ====================

def create_access_token(user_id: int, openid: str) -> str:
    """生成 JWT Token"""
    from jose import jwt
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    payload = {
        "sub": str(user_id),
        "openid": openid,
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


async def get_current_user_id(authorization: str = Header(...)) -> int:
    """从 Authorization header 解析当前用户 ID"""
    from jose import jwt, JWTError
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="无效的认证信息")
    token = authorization[7:]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Token 已过期或无效")


async def get_current_admin(authorization: str = Header(...)) -> dict:
    """验证当前用户是否为管理员，返回用户信息"""
    user_id = await get_current_user_id(authorization)
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT u.id, u.openid, u.nickname, u.role, a.role as admin_role FROM users u LEFT JOIN admins a ON u.id = a.user_id WHERE u.id = ?",
            (user_id,)
        )
        user = await cursor.fetchone()
        if not user or not user["admin_role"]:
            raise HTTPException(status_code=403, detail="需要管理员权限")
        return dict(user)
    finally:
        await db.close()


# ==================== 路由 ====================

@router.post("/login")
async def wechat_login(req: WechatLoginRequest):
    """微信授权登录"""
    try:
        session_data = await code2session(req.code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"微信登录失败: {str(e)}")

    openid = session_data["openid"]
    session_key = session_data["session_key"]
    unionid = session_data.get("unionid", "")

    now = datetime.now().isoformat()
    db = await get_db()
    try:
        cursor = await db.execute("SELECT id FROM users WHERE openid = ?", (openid,))
        user = await cursor.fetchone()

        if user:
            await db.execute(
                "UPDATE users SET session_key = ?, union_id = ?, updated_at = ? WHERE openid = ?",
                (session_key, unionid, now, openid)
            )
            await db.commit()
            user_id = user["id"]
        else:
            cursor = await db.execute(
                "INSERT INTO users (openid, session_key, union_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (openid, session_key, unionid, now, now)
            )
            await db.commit()
            user_id = cursor.lastrowid

        token = create_access_token(user_id, openid)
        return {"token": token, "user_id": user_id}
    finally:
        await db.close()


@router.post("/admin-login")
async def admin_login(req: AdminLoginRequest):
    """管理员密码登录"""
    if req.password != settings.ADMIN_INIT_PASSWORD:
        raise HTTPException(status_code=401, detail="密码错误")

    # 查找或创建超级管理员用户
    now = datetime.now().isoformat()
    db = await get_db()
    try:
        cursor = await db.execute("SELECT id FROM users WHERE openid = 'super_admin'")
        user = await cursor.fetchone()

        if user:
            user_id = user["id"]
        else:
            cursor = await db.execute(
                "INSERT INTO users (openid, nickname, role, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                ("super_admin", "超级管理员", "super_admin", now, now)
            )
            await db.commit()
            user_id = cursor.lastrowid

        # 确保管理员记录存在
        await db.execute(
            "INSERT OR IGNORE INTO admins (user_id, role, created_at) VALUES (?, ?, ?)",
            (user_id, "super_admin", now)
        )
        await db.commit()

        token = create_access_token(user_id, "super_admin")
        return {"token": token, "user_id": user_id, "role": "super_admin"}
    finally:
        await db.close()
