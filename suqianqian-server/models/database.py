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
    "通用AI能力": {
        "sub": ["角色设定Skill", "思维链CoT", "自我校验Skill", "RAG问答优化", "长文本处理"]
    },
    "文案内容创作": {
        "sub": ["短视频脚本", "公众号文案", "海报文案", "公文写作"]
    },
    "网文小说专用": {
        "sub": ["人物设定锁死Skill", "剧情逻辑自检", "章节润色", "伏笔埋点工具", "文风统一Skill", "小说审稿纠错"]
    },
    "程序/测试/运维": {
        "sub": ["代码生成", "代码解释", "测试用例", "运维巡检SOP", "服务器脚本"]
    },
    "办公自动化SOP": {
        "sub": ["Excel分析", "PPT大纲", "周报月报", "会议纪要"]
    },
    "学习科研助手": {
        "sub": ["论文润色", "文献总结", "思维导图生成"]
    },
    "行业垂直Skill": {
        "sub": ["电商运营", "教育", "心理咨询", "职场咨询"]
    },
    "Agent工作流模板": {
        "sub": ["Dify工作流", "OpenWebUI Pipeline", "Ollama角色Skill"]
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
