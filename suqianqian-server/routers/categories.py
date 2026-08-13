"""
AI Skill 库 - 分类路由
分类数据从数据库 skills 表自动聚合，无需手动维护
"""
from fastapi import APIRouter
from models.database import get_db

router = APIRouter()


@router.get("")
async def get_categories():
    """获取分类树（从数据库自动聚合）"""
    db = await get_db()
    try:
        # 从 skills 表聚合出分类树
        cur = await db.execute("""
            SELECT category, sub_category, COUNT(*) as cnt
            FROM skills
            WHERE status = 'published'
            GROUP BY category, sub_category
            ORDER BY category, cnt DESC
        """)
        rows = await cur.fetchall()

        # 组装树状结构
        cat_map = {}
        for row in rows:
            cat = row[0]
            sub = row[1] or ""
            cnt = row[2]
            if cat not in cat_map:
                cat_map[cat] = {"name": cat, "sub_categories": [], "total": 0}
            if sub:
                cat_map[cat]["sub_categories"].append(sub)
            cat_map[cat]["total"] += cnt

        # 按数量排序大类
        result = sorted(cat_map.values(), key=lambda x: -x["total"])
        return {"categories": result}
    finally:
        await db.close()
