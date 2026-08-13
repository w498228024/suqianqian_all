"""
AI Skill 库 - 分类路由
"""
from fastapi import APIRouter
from models.database import CATEGORIES

router = APIRouter()


@router.get("")
async def get_categories():
    """获取分类树"""
    result = []
    for name, data in CATEGORIES.items():
        result.append({
            "name": name,
            "sub_categories": data["sub"],
        })
    return {"categories": result}
