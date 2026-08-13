"""
数签签 - 后端通用日志工具
通过 LOG_ENABLED 开关控制全局日志输出
"""
import logging
import sys
from config import settings

# ==================== 日志开关 ====================
LOG_ENABLED = True

# 配置日志格式
logger = logging.getLogger("suqianqian")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log(tag: str, msg: str, data=None):
    """通用日志"""
    if not LOG_ENABLED:
        return
    if data is not None:
        logger.info(f"[{tag}] {msg} | {data}")
    else:
        logger.info(f"[{tag}] {msg}")


def log_error(tag: str, msg: str, data=None):
    """错误日志"""
    if not LOG_ENABLED:
        return
    if data is not None:
        logger.error(f"[{tag}] {msg} | {data}")
    else:
        logger.error(f"[{tag}] {msg}")
