# 数签签 - AI 智能识别工具小程序

基于微信小程序 + FastAPI 后端 + 多模态大模型的签签数量识别工具。

## 技术架构

```
┌─────────────────────────────────────────────────┐
│                  微信小程序（前端）                │
│  Skyline 渲染器 / glass-easel 组件框架            │
│  页面: login → home → result                     │
└──────────────────────┬──────────────────────────┘
                       │ HTTPS / JSON
┌──────────────────────▼──────────────────────────┐
│              FastAPI 后端服务                      │
│  ┌──────────┐  ┌───────────┐  ┌──────────────┐  │
│  │ 认证路由  │  │ 识别路由   │  │  次数限制     │  │
│  │ /api/auth│  │/api/recogn │  │  可配置额度   │  │
│  └──────────┘  └───────────┘  └──────────────┘  │
│  ┌──────────────────────────────────────────┐    │
│  │         大模型调度层 (llm_service)         │    │
│  │   根据 LLM_PROVIDER 配置自动路由          │    │
│  └─────┬──────────┬──────────┬─────────────┘    │
│        │          │          │                    │
│  ┌─────▼───┐ ┌───▼────┐ ┌──▼────────┐          │
│  │ 文心一言 │ │  Kimi  │ │ DeepSeek  │ ...      │
│  │ wenxin  │ │  kimi  │ │ deepseek  │          │
│  └─────────┘ └────────┘ └───────────┘          │
│  ┌──────────────────────────────────────────┐    │
│  │          SQLite 数据库                     │    │
│  │  users 表  |  recognition_logs 表         │    │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

## 目录结构

```
suqianqian/
├── app.js / app.json / app.wxss     # 小程序全局配置
├── pages/
│   ├── login/                        # 登录页（微信一键登录 + 手机号）
│   ├── home/                         # 首页（拍照/图库 + 次数展示）
│   └── result/                       # 结果页（标注图 + 保存 + 分享）
├── utils/
│   └── request.js                    # 网络请求封装（token 注入、错误处理）
├── images/                           # 静态图片资源
│
└── server/                           # 后端服务
    ├── main.py                       # FastAPI 入口
    ├── config.py                     # 全局配置（模型/次数/微信）
    ├── requirements.txt              # Python 依赖
    ├── models/database.py            # 数据库模型（SQLite）
    ├── routers/
    │   ├── auth.py                   # 认证路由（登录/手机号绑定）
    │   └── recognize.py              # 识别路由（上传/识别/次数限制）
    ├── services/
    │   ├── wechat_service.py         # 微信开放平台交互
    │   └── llm_service.py            # 大模型调度层
    ├── providers/                    # 模型供应商（可插拔）
    │   ├── base_provider.py          # 抽象基类
    │   ├── wenxin_provider.py        # 百度文心一言
    │   ├── kimi_provider.py          # Kimi（月之暗面）
    │   └── deepseek_provider.py      # DeepSeek Vision
    └── uploads/                      # 图片临时存储
```

## 核心特性

- **通用型大模型对接**：通过配置切换模型供应商（wenxin / kimi / deepseek），业务代码零改动
- **每日次数限制**：可配置每日识别次数上限，前后端双重校验
- **微信一键登录**：wx.login + getPhoneNumber，JWT Token 鉴权
- **拍照/图库上传**：兼容 iOS / Android / HarmonyOS 权限弹窗
- **AI 标注返回**：在原图上绘制识别框，支持保存到相册
- **Agent 规范提示词**：非符合规则图片直接拒绝，保证识别质量

## 快速开始

### 后端

```bash
cd server
pip install -r requirements.txt

# 配置环境变量
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret
export DEEPSEEK_API_KEY=your_deepseek_api_key
export LLM_PROVIDER=deepseek

# 启动服务
python main.py
# 访问 http://localhost:8000 查看 API 文档
```

### 前端

1. 微信开发者工具打开项目根目录
2. 修改 `utils/request.js` 中的 `BASE_URL` 为后端地址
3. 编译预览

## 配置说明

所有配置集中在 `server/config.py`，支持环境变量覆盖：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `LLM_PROVIDER` | 模型供应商 | `wenxin` |
| `DAILY_RECOGNIZE_LIMIT` | 每日识别次数 | `10` |
| `WECHAT_APP_ID` | 小程序 AppID | - |
| `WECHAT_APP_SECRET` | 小程序 AppSecret | - |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | - |
| `KIMI_API_KEY` | Kimi API Key | - |
| `WENXIN_API_KEY` | 文心一言 API Key | - |
| `WENXIN_SECRET_KEY` | 文心一言 Secret Key | - |
| `JWT_SECRET_KEY` | JWT 签名密钥 | - |
| `MAX_IMAGE_SIZE_MB` | 最大图片大小 | `10` |

## 文档

- [API 接口文档](./API.md)
- [部署指南](./DEPLOY.md)
