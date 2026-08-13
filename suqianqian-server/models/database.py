"""
AI Skill 库 - 数据库模型与初始化
"""
import aiosqlite
import os
import json
from datetime import datetime

DATABASE_PATH = "suqianqian.db"


async def get_db() -> aiosqlite.Connection:
    """获取数据库连接"""
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    return db


# ==================== 分类数据 ====================

CATEGORIES = {
    "程序开发": {
        "sub": ["前端开发", "后端开发", "移动开发", "DevOps/运维", "测试/QA", "AI/ML开发", "安全/加密", "代码工具"]
    },
    "医疗健康": {
        "sub": ["中医养生", "西医问诊", "心理健康", "健身运动", "营养饮食", "儿科/妇产", "牙科/眼科"]
    },
    "法律合规": {
        "sub": ["合同审查", "劳动法律", "知识产权", "法律咨询"]
    },
    "金融财经": {
        "sub": ["投资理财", "税务筹划", "财务分析", "保险规划"]
    },
    "电商运营": {
        "sub": ["商品优化", "直播带货", "跨境电商", "店铺运营"]
    },
    "自媒体营销": {
        "sub": ["小红书", "短视频", "公众号/博客", "品牌营销", "社交媒体", "SEO/SEM"]
    },
    "教育学习": {
        "sub": ["语言学习", "考试备考", "学术论文", "K12教育", "学习方法"]
    },
    "办公效率": {
        "sub": ["Excel/数据", "PPT/演示", "公文/报告", "会议管理", "文档写作"]
    },
    "职场求职": {
        "sub": ["简历优化", "面试准备", "职业规划", "招聘HR"]
    },
    "设计创意": {
        "sub": ["UI/UX设计", "平面/视觉", "摄影摄像", "音乐/音频"]
    },
    "写作创作": {
        "sub": ["小说写作", "编剧/剧本", "诗歌散文", "创意写作"]
    },
    "生活服务": {
        "sub": ["旅行规划", "宠物养护", "穿搭造型", "情感关系"]
    },
    "客服售后": {
        "sub": ["售前咨询", "售后/投诉"]
    },
    "餐饮行业": {
        "sub": ["菜单策划", "食品安全", "烹饪食谱"]
    },
    "房产建筑": {
        "sub": ["房产投资", "室内设计"]
    },
    "农业": {
        "sub": ["种植养殖"]
    },
    "供应链物流": {
        "sub": ["质量管理", "供应链/物流", "生产制造"]
    },
    "通用AI能力": {
        "sub": ["角色扮演", "思维训练", "提示工程", "AI工具使用", "游戏/娱乐", "翻译/语言", "效率工具"]
    },
}

FIT_TOOLS = ["Ollama", "OpenWebUI", "Dify", "其他"]

SOURCE_TYPES = ["原创", "开源改编", "用户投稿"]

LICENSES = ["MIT", "Apache2.0", "原创版权", "其他"]


async def init_db():
    """初始化数据库表"""
    db = await get_db()
    try:
        # 用户表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                openid TEXT UNIQUE NOT NULL,
                session_key TEXT,
                union_id TEXT DEFAULT '',
                nickname TEXT DEFAULT '',
                avatar_url TEXT DEFAULT '',
                role TEXT DEFAULT 'user',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Skill 表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                desc TEXT DEFAULT '',
                content TEXT DEFAULT '',
                category TEXT NOT NULL,
                sub_category TEXT DEFAULT '',
                tags TEXT DEFAULT '[]',
                fit_tools TEXT DEFAULT '[]',
                author TEXT DEFAULT '',
                source_type TEXT DEFAULT '原创',
                license TEXT DEFAULT 'MIT',
                collect_num INTEGER DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending',
                uploader_id INTEGER,
                reviewer_id INTEGER,
                review_note TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (uploader_id) REFERENCES users(id)
            )
        """)

        # 收藏表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                skill_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(user_id, skill_id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (skill_id) REFERENCES skills(id)
            )
        """)

        # 管理员表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                role TEXT DEFAULT 'admin',
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # 系统设置表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT DEFAULT ''
            )
        """)

        # 初始化默认设置
        await db.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            ("ad_enabled", "false")
        )
        await db.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            ("total_uv", "0")
        )

        await db.commit()
        print("数据库初始化完成")
    finally:
        await db.close()
