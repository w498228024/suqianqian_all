"""
AI Skill 库 - FastAPI 后端入口
"""
import os
import json
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings
from models.database import init_db
from utils.logger import log, log_error


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    os.makedirs("admin", exist_ok=True)
    yield


app = FastAPI(
    title="AI Skill 库 API",
    description="Skill 文本素材平台",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== 日志中间件 ====================

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        method = request.method
        path = request.url.path

        req_body = None
        if method in ("POST", "PUT", "PATCH"):
            try:
                body = await request.body()
                if body:
                    req_body = body.decode("utf-8", errors="replace")
                    try:
                        req_body = json.loads(req_body)
                    except json.JSONDecodeError:
                        req_body = f"<binary {len(body)} bytes>"
            except Exception:
                req_body = "<read failed>"

        safe_body = self._sanitize(req_body)
        log("API", f"{method} {path} 请求", safe_body)

        try:
            response = await call_next(request)
        except Exception as e:
            log_error("API", f"{method} {path} 异常", str(e))
            raise

        resp_body = b""
        async for chunk in response.body_iterator:
            resp_body += chunk

        resp_data = None
        try:
            resp_data = json.loads(resp_body.decode("utf-8"))
        except Exception:
            resp_data = f"<binary {len(resp_body)} bytes>"

        elapsed = round((time.time() - start) * 1000)
        log("API", f"{method} {path} 响应 [{response.status_code}] ({elapsed}ms)", resp_data)

        from starlette.responses import Response as StarletteResponse
        return StarletteResponse(
            content=resp_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    def _sanitize(self, data):
        if isinstance(data, dict):
            return {
                k: "***" if k.lower() in ("token", "secret", "password", "authorization") else v
                for k, v in data.items()
            }
        return data


app.add_middleware(LoggingMiddleware)

# ==================== 注册路由 ====================

from routers import auth, skills, categories, admin, settings

app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skill"])
app.include_router(categories.router, prefix="/api/categories", tags=["分类"])
app.include_router(admin.router, prefix="/api/admin", tags=["管理"])
app.include_router(settings.router, prefix="/api/settings", tags=["设置"])

# 管理后台静态文件
if os.path.isdir("admin"):
    app.mount("/admin", StaticFiles(directory="admin", html=True), name="admin")


@app.get("/")
async def root():
    return {"message": "AI Skill 库 API 服务运行中", "version": "2.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
