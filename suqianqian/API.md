# 数签签 - API 接口文档

Base URL: `http://localhost:8000`（开发环境）

启动后访问 `http://localhost:8000/docs` 可查看 Swagger 交互式文档。

---

## 通用说明

### 鉴权方式

需要鉴权的接口在 Header 中传入：
```
Authorization: Bearer <token>
```

### 统一错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

| HTTP 状态码 | 含义 |
|-------------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未登录或 Token 过期 |
| 403 | 操作受限（如识别次数用完） |
| 500 | 服务端错误 |

---

## 健康检查

### GET /

```bash
curl http://localhost:8000/
```

**响应：**
```json
{
  "message": "数签签 API 服务运行中",
  "version": "1.0.0"
}
```

### GET /health

```bash
curl http://localhost:8000/health
```

**响应：**
```json
{
  "status": "ok"
}
```

---

## 认证模块 `/api/auth`

### POST /api/auth/login — 微信一键登录

通过 `wx.login()` 获取的 code 换取 JWT Token。

**请求：**
```json
{
  "code": "0a3Xyz000abc123"
}
```

**响应：**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "openid": "oXXXX...",
  "is_new_user": true
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| token | string | JWT Token，后续接口需携带 |
| openid | string | 微信用户唯一标识 |
| is_new_user | bool | 是否新用户 |

---

### POST /api/auth/bindPhoneWithToken — 绑定手机号

需要鉴权。通过 `getPhoneNumber` 组件获取的 code 换取手机号。

**Header：**
```
Authorization: Bearer <token>
```

**请求：**
```json
{
  "code": "getPhoneNumber_code_xxx"
}
```

**响应：**
```json
{
  "phone": "13800138000"
}
```

---

## 识别模块 `/api/recognize`

### GET /api/recognize/quota — 查询剩余识别次数

需要鉴权。返回用户今日识别次数配额。

**Header：**
```
Authorization: Bearer <token>
```

**响应：**
```json
{
  "daily_limit": 10,
  "used_today": 3,
  "remaining": 7
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| daily_limit | int | 每日上限（可配置） |
| used_today | int | 今日已用次数 |
| remaining | int | 剩余次数 |

---

### POST /api/recognize/ — 上传图片并识别

需要鉴权。上传图片，调用大模型识别签签数量，返回标注后的图片。

**Header：**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | File | 是 | 图片文件（jpg/png，最大 10MB） |

**curl 示例：**
```bash
curl -X POST http://localhost:8000/api/recognize/ \
  -H "Authorization: Bearer <token>" \
  -F "file=@/path/to/image.jpg"
```

**成功响应（识别到物品）：**
```json
{
  "found": true,
  "count": 15,
  "message": "识别完成",
  "items": [
    {"label": "签签", "bbox": [120, 50, 145, 380]},
    {"label": "签签", "bbox": [160, 45, 185, 375]},
    ...
  ],
  "annotated_image_url": "/static/uploads/annotated_abc123.jpg",
  "remaining_count": 6
}
```

**成功响应（未识别到物品）：**
```json
{
  "found": false,
  "count": 0,
  "message": "未发现签签等相关内容",
  "items": [],
  "annotated_image_url": null,
  "remaining_count": 6
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| found | bool | 是否发现签签 |
| count | int | 识别到的数量 |
| message | string | 提示信息 |
| items | array | 识别到的物品列表（含标签和坐标） |
| annotated_image_url | string/null | 标注图片路径（拼接 baseUrl 访问） |
| remaining_count | int | 今日剩余识别次数 |

**错误响应：**

| 场景 | 状态码 | detail |
|------|--------|--------|
| 未登录 | 401 | Token 已过期或无效 |
| 次数用完 | 403 | 今日识别次数已用完（上限 10 次/天），请明日再试 |
| 文件类型错误 | 400 | 请上传图片文件 |
| 文件过大 | 400 | 图片大小不能超过 10MB |
| 模型调用失败 | 500 | 识别失败: ... |

---

## 静态资源

标注后的图片通过静态文件服务访问：

```
GET /static/uploads/annotated_<uuid>.jpg
```

完整 URL 示例：`http://localhost:8000/static/uploads/annotated_abc123.jpg`

---

## 切换模型供应商

修改环境变量或 `config.py`：

```bash
# 使用 DeepSeek
export LLM_PROVIDER=deepseek
export DEEPSEEK_API_KEY=sk-xxx

# 使用 Kimi
export LLM_PROVIDER=kimi
export KIMI_API_KEY=sk-xxx

# 使用文心一言
export LLM_PROVIDER=wenxin
export WENXIN_API_KEY=xxx
export WENXIN_SECRET_KEY=xxx
```

重启后端服务即可生效，前端代码无需任何改动。
