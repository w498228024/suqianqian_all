"""
AI Skill 库 - 后端配置文件
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ==================== 微信小程序配置 ====================
    WECHAT_APP_ID: str = os.getenv("WECHAT_APP_ID", "wxb344dfb2dc09e81c")
    WECHAT_APP_SECRET: str = os.getenv("WECHAT_APP_SECRET", "2b0520fd1d26d0150142b70424fa4b12")

    # ==================== JWT 配置 ====================
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24 * 7  # 7天过期

    # ==================== 管理员配置 ====================
    ADMIN_INIT_PASSWORD: str = os.getenv("ADMIN_INIT_PASSWORD", "admin123456")

    # ==================== 数据库 ====================
    # 云托管环境通过环境变量 DATABASE_PATH 指定 db 文件路径（如 /data/suqianqian.db）
    # 本地开发默认使用项目目录下的 suqianqian.db
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "./suqianqian.db")
    DATABASE_URL: str = "sqlite+aiosqlite:///" + os.getenv("DATABASE_PATH", "./suqianqian.db")

    # ==================== 分页配置 ====================
    PAGE_SIZE: int = 20


settings = Settings()
