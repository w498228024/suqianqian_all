# 数签签 - 部署指南

## 一、环境要求

| 组件 | 最低版本 | 说明 |
|------|----------|------|
| Python | 3.9+ | 后端运行环境 |
| 微信开发者工具 | 最新稳定版 | 小程序开发调试 |
| 服务器 | 1核2G+ | 生产环境部署 |
| 域名 | 已备案 | 小程序要求 HTTPS |
| SSL 证书 | - | HTTPS 必需 |

---

## 二、后端部署

### 2.1 服务器准备

```bash
# 安装 Python 3.9+
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 创建项目目录
mkdir -p /opt/suqianqian
cd /opt/suqianqian

# 上传项目代码（git clone 或 scp）
```

### 2.2 创建虚拟环境 & 安装依赖

```bash
cd /opt/suqianqian/server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2.3 配置环境变量

创建 `.env` 文件（或直接在系统中 export）：

```bash
cat > /opt/suqianqian/server/.env << 'EOF'
# 微信小程序
WECHAT_APP_ID=wx_your_app_id
WECHAT_APP_SECRET=your_app_secret

# JWT 密钥（务必修改为随机字符串）
JWT_SECRET_KEY=your-random-secret-key-at-least-32-chars

# 大模型（选择其中一个）
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-deepseek-key

# 识别次数限制
DAILY_RECOGNIZE_LIMIT=10
EOF
```

### 2.4 使用 Gunicorn + Uvicorn 运行

```bash
# 安装 gunicorn
pip install gunicorn

# 启动（4 个 worker）
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  --access-logfile /var/log/suqianqian/access.log \
  --error-logfile /var/log/suqianqian/error.log
```

### 2.5 使用 Systemd 管理进程

```bash
sudo cat > /etc/systemd/system/suqianqian.service << 'EOF'
[Unit]
Description=SuQianQian FastAPI Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/suqianqian/server
Environment="PATH=/opt/suqianqian/server/venv/bin"
ExecStart=/opt/suqianqian/server/venv/bin/gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable suqianqian
sudo systemctl start suqianqian
sudo systemctl status suqianqian
```

### 2.6 Nginx 反向代理（HTTPS）

```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate     /etc/nginx/ssl/yourdomain.pem;
    ssl_certificate_key /etc/nginx/ssl/yourdomain.key;

    # 图片上传大小限制
    client_max_body_size 15m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 识别接口可能耗时较长
        proxy_read_timeout 120s;
        proxy_connect_timeout 10s;
    }
}

# HTTP 重定向
server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$host$request_uri;
}
```

```bash
sudo nginx -t && sudo systemctl reload nginx
```

---

## 三、小程序配置

### 3.1 修改后端地址

编辑 `utils/request.js`，将 `BASE_URL` 改为生产域名：

```javascript
const BASE_URL = 'https://api.yourdomain.com'
```

### 3.2 配置服务器域名

在微信公众平台 → 开发管理 → 开发设置 → 服务器域名：

| 类型 | 域名 |
|------|------|
| request 合法域名 | `https://api.yourdomain.com` |
| uploadFile 合法域名 | `https://api.yourdomain.com` |

### 3.3 配置业务域名（如需要）

如果涉及 webview 页面，需在微信公众平台配置业务域名。

---

## 四、微信小程序后台配置

### 4.1 获取手机号权限

在微信公众平台 → 开发管理 → 接口设置 中：
- 确认已开通「手机号快速验证」权限
- 确认已开通「获取手机号」权限

### 4.2 发布上线

```bash
# 1. 在微信开发者工具中上传代码
# 2. 登录微信公众平台
# 3. 版本管理 → 开发版本 → 提交审核
# 4. 审核通过后发布
```

---

## 五、运维检查

### 5.1 日志查看

```bash
# 应用日志
sudo journalctl -u suqianqian -f

# Nginx 日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 5.2 数据库备份

```bash
# SQLite 数据库位于 /opt/suqianqian/server/suqianqian.db
# 定时备份
crontab -e
# 每天凌晨 3 点备份
0 3 * * * cp /opt/suqianqian/server/suqianqian.db /opt/backups/suqianqian_$(date +\%Y\%m\%d).db
```

### 5.3 健康检查

```bash
curl https://api.yourdomain.com/health
# 预期返回: {"status":"ok"}
```

---

## 六、常见问题

| 问题 | 解决方案 |
|------|----------|
| 小程序请求失败 | 检查域名是否已备案、SSL 证书是否有效、服务器域名是否已配置 |
| 图片上传失败 | 检查 Nginx `client_max_body_size` 配置 |
| 识别超时 | 调大 `proxy_read_timeout`，检查大模型 API 连通性 |
| Token 过期 | 前端自动跳转登录页重新获取 |
| 次数限制不生效 | 检查 `DAILY_RECOGNIZE_LIMIT` 配置，确认时区一致 |
