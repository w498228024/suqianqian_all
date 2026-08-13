"""
AI Skill 库 - 系统设置路由（小程序端）
"""
from fastapi import APIRouter
from models.database import get_db

router = APIRouter()


@router.get("/ad-switch")
async def get_ad_switch():
    """获取广告开关状态"""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT value FROM settings WHERE key = 'ad_enabled'")
        row = await cursor.fetchone()
        enabled = row["value"] == "true" if row else False
        return {"ad_enabled": enabled}
    finally:
        await db.close()
