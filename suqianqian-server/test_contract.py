"""
AI Skill 库 - 全栈契约测试
覆盖：后端 API 接口 + 小程序前端代码静态检查
"""
import httpx
import json
import os
import re
import sys
from pathlib import Path

# ==================== 配置 ====================
BASE_URL = "https://flask-p0w8-296442-11-1453433457.sh.run.tcloudbase.com"
PROJECT_ROOT = Path(__file__).parent.parent  # suqianqian_all/
MINIPROGRAM_DIR = PROJECT_ROOT / "suqianqian"
SERVER_DIR = PROJECT_ROOT / "suqianqian-server"

# 颜色输出
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

stats = {"passed": 0, "failed": 0, "skipped": 0}
errors = []


def log_result(status, name, detail=""):
    """记录测试结果"""
    if status == "PASS":
        print(f"  {GREEN}✓ PASS{RESET}  {name}")
        stats["passed"] += 1
    elif status == "FAIL":
        print(f"  {RED} FAIL{RESET}  {name}")
        if detail:
            print(f"         {detail}")
        stats["failed"] += 1
        errors.append(name)
    elif status == "SKIP":
        print(f"  {YELLOW} SKIP{RESET}  {name}")
        stats["skipped"] += 1


# =====================================================================
# Part 1: 后端 API 契约测试
# =====================================================================

def test_backend_api():
    """测试后端 API 接口"""
    print(f"\n{CYAN}{'='*60}")
    print(f"Part 1: 后端 API 契约测试")
    print(f"目标: {BASE_URL}")
    print(f"{'='*60}{RESET}\n")

    # ---------- 1.1 基础接口 ----------
    print("【1.1 基础接口】")
    
    # GET /
    try:
        resp = httpx.get(f"{BASE_URL}/", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if "message" in data and "version" in data:
                log_result("PASS", "GET / 根路径")
            else:
                log_result("FAIL", "GET / 根路径", "响应格式错误")
        else:
            log_result("FAIL", "GET / 根路径", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "GET / 根路径", str(e))

    # GET /health
    try:
        resp = httpx.get(f"{BASE_URL}/health", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "ok":
                log_result("PASS", "GET /health 健康检查")
            else:
                log_result("FAIL", "GET /health 健康检查", "status != ok")
        else:
            log_result("FAIL", "GET /health 健康检查", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "GET /health 健康检查", str(e))

    # ---------- 1.2 分类接口 ----------
    print("\n【1.2 分类接口】")
    try:
        resp = httpx.get(f"{BASE_URL}/api/categories", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if "categories" in data and isinstance(data["categories"], list):
                log_result("PASS", "GET /api/categories 分类树")
            else:
                log_result("FAIL", "GET /api/categories 分类树", "响应格式错误")
        else:
            log_result("FAIL", "GET /api/categories 分类树", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "GET /api/categories 分类树", str(e))

    # ---------- 1.3 Skill 列表 ----------
    print("\n【1.3 Skill 列表】")
    
    # 默认列表
    try:
        resp = httpx.get(f"{BASE_URL}/api/skills?page=1&page_size=5", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if all(k in data for k in ["items", "total", "page"]) and isinstance(data["items"], list):
                log_result("PASS", "GET /api/skills 默认列表")
            else:
                log_result("FAIL", "GET /api/skills 默认列表", "响应格式错误")
        else:
            log_result("FAIL", "GET /api/skills 默认列表", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "GET /api/skills 默认列表", str(e))

    # 按分类筛选
    try:
        resp = httpx.get(f"{BASE_URL}/api/skills?category=通用 AI 能力&page_size=3", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if all(s["category"] == "通用 AI 能力" for s in data.get("items", [])):
                log_result("PASS", "GET /api/skills?category= 分类筛选")
            else:
                log_result("FAIL", "GET /api/skills?category= 分类筛选", "筛选结果不匹配")
        else:
            log_result("FAIL", "GET /api/skills?category= 分类筛选", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "GET /api/skills?category= 分类筛选", str(e))

    # ---------- 1.4 Skill 详情 ----------
    print("\n【1.4 Skill 详情】")
    
    # 获取首个 ID
    first_id = None
    try:
        resp = httpx.get(f"{BASE_URL}/api/skills?page=1&page_size=1", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("items"):
                first_id = data["items"][0]["id"]
    except:
        pass

    if first_id:
        # 正常详情
        try:
            resp = httpx.get(f"{BASE_URL}/api/skills/{first_id}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if all(k in data for k in ["id", "title", "content", "tags", "fit_tools"]):
                    log_result("PASS", f"GET /api/skills/{{id}} 详情 (id={first_id})")
                else:
                    log_result("FAIL", f"GET /api/skills/{{id}} 详情", "响应字段缺失")
            else:
                log_result("FAIL", f"GET /api/skills/{{id}} 详情", f"状态码 {resp.status_code}")
        except Exception as e:
            log_result("FAIL", f"GET /api/skills/{{id}} 详情", str(e))

        # 不存在的 ID
        try:
            resp = httpx.get(f"{BASE_URL}/api/skills/99999", timeout=10)
            if resp.status_code == 404:
                log_result("PASS", "GET /api/skills/99999 不存在返回 404")
            else:
                log_result("FAIL", "GET /api/skills/99999 不存在返回 404", f"状态码 {resp.status_code}")
        except Exception as e:
            log_result("FAIL", "GET /api/skills/99999 不存在返回 404", str(e))
    else:
        log_result("SKIP", "Skill 详情测试", "无有效 ID")

    # ---------- 1.5 搜索接口 ----------
    print("\n【1.5 搜索接口】")
    
    # 正常搜索
    try:
        resp = httpx.get(f"{BASE_URL}/api/skills/search/list?keyword=代码&page=1&page_size=5", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if "items" in data and data.get("keyword") == "代码":
                log_result("PASS", "GET /api/skills/search/list 搜索")
            else:
                log_result("FAIL", "GET /api/skills/search/list 搜索", "响应格式错误")
        else:
            log_result("FAIL", "GET /api/skills/search/list 搜索", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "GET /api/skills/search/list 搜索", str(e))

    # 无结果搜索
    try:
        resp = httpx.get(f"{BASE_URL}/api/skills/search/list?keyword=xyznotfound&page=1", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("total", -1) == 0:
                log_result("PASS", "GET /api/skills/search/list 无结果")
            else:
                log_result("FAIL", "GET /api/skills/search/list 无结果", "total != 0")
        else:
            log_result("FAIL", "GET /api/skills/search/list 无结果", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "GET /api/skills/search/list 无结果", str(e))

    # ---------- 1.6 设置接口 ----------
    print("\n【1.6 设置接口】")
    try:
        resp = httpx.get(f"{BASE_URL}/api/settings/ad-switch", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if "ad_enabled" in data:
                log_result("PASS", "GET /api/settings/ad-switch 广告开关")
            else:
                log_result("FAIL", "GET /api/settings/ad-switch 广告开关", "响应格式错误")
        else:
            log_result("FAIL", "GET /api/settings/ad-switch 广告开关", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "GET /api/settings/ad-switch 广告开关", str(e))

    # ---------- 1.7 登录接口 ----------
    print("\n【1.7 登录接口】")
    
    # 微信登录 (无效 code)
    try:
        resp = httpx.post(f"{BASE_URL}/api/auth/login", json={"code": "invalid_test"}, timeout=10)
        if resp.status_code == 400:
            log_result("PASS", "POST /api/auth/login 无效 code 返回 400")
        else:
            log_result("FAIL", "POST /api/auth/login 无效 code 返回 400", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "POST /api/auth/login 无效 code 返回 400", str(e))

    # 管理员登录 (错误密码)
    try:
        resp = httpx.post(f"{BASE_URL}/api/auth/admin-login", json={"password": "wrong"}, timeout=10)
        if resp.status_code == 401:
            log_result("PASS", "POST /api/auth/admin-login 错误密码返回 401")
        else:
            log_result("FAIL", "POST /api/auth/admin-login 错误密码返回 401", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "POST /api/auth/admin-login 错误密码返回 401", str(e))

    # 管理员登录 (正确密码)
    admin_token = None
    try:
        resp = httpx.post(f"{BASE_URL}/api/auth/admin-login", json={"password": "admin123456"}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("token"):
                admin_token = data["token"]
                log_result("PASS", "POST /api/auth/admin-login 管理员登录")
            else:
                log_result("FAIL", "POST /api/auth/admin-login 管理员登录", "无 token")
        else:
            log_result("FAIL", "POST /api/auth/admin-login 管理员登录", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "POST /api/auth/admin-login 管理员登录", str(e))

    # ---------- 1.8 需要认证的接口 ----------
    print("\n【1.8 需要认证的接口】")
    
    if admin_token:
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        # 收藏
        if first_id:
            try:
                resp = httpx.post(f"{BASE_URL}/api/skills/{first_id}/collect", headers=headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if "collected" in data:
                        log_result("PASS", "POST /api/skills/{{id}}/collect 收藏")
                    else:
                        log_result("FAIL", "POST /api/skills/{{id}}/collect 收藏", "响应格式错误")
                else:
                    log_result("FAIL", "POST /api/skills/{{id}}/collect 收藏", f"状态码 {resp.status_code}")
            except Exception as e:
                log_result("FAIL", "POST /api/skills/{{id}}/collect 收藏", str(e))

            # 收藏状态
            try:
                resp = httpx.get(f"{BASE_URL}/api/skills/favorites/status?skill_id={first_id}", headers=headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if "is_favorited" in data:
                        log_result("PASS", "GET /api/skills/favorites/status 收藏状态")
                    else:
                        log_result("FAIL", "GET /api/skills/favorites/status 收藏状态", "响应格式错误")
                else:
                    log_result("FAIL", "GET /api/skills/favorites/status 收藏状态", f"状态码 {resp.status_code}")
            except Exception as e:
                log_result("FAIL", "GET /api/skills/favorites/status 收藏状态", str(e))

            # 收藏列表
            try:
                resp = httpx.get(f"{BASE_URL}/api/skills/favorites/list?page=1", headers=headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if "items" in data and "total" in data:
                        log_result("PASS", "GET /api/skills/favorites/list 收藏列表")
                    else:
                        log_result("FAIL", "GET /api/skills/favorites/list 收藏列表", "响应格式错误")
                else:
                    log_result("FAIL", "GET /api/skills/favorites/list 收藏列表", f"状态码 {resp.status_code}")
            except Exception as e:
                log_result("FAIL", "GET /api/skills/favorites/list 收藏列表", str(e))

            # 取消收藏
            try:
                resp = httpx.post(f"{BASE_URL}/api/skills/{first_id}/collect", headers=headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("collected") == False:
                        log_result("PASS", "POST /api/skills/{{id}}/collect 取消收藏")
                    else:
                        log_result("FAIL", "POST /api/skills/{{id}}/collect 取消收藏", "collected != False")
                else:
                    log_result("FAIL", "POST /api/skills/{{id}}/collect 取消收藏", f"状态码 {resp.status_code}")
            except Exception as e:
                log_result("FAIL", "POST /api/skills/{{id}}/collect 取消收藏", str(e))
        else:
            log_result("SKIP", "收藏相关测试", "无有效 Skill ID")

        # 创建 Skill
        try:
            resp = httpx.post(f"{BASE_URL}/api/skills", headers=headers, json={
                "title": "契约测试 Skill",
                "desc": "自动化测试",
                "content": "# 测试",
                "category": "通用 AI 能力",
                "tags": ["测试"],
                "fit_tools": ["Ollama"],
            }, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if "id" in data and "message" in data:
                    log_result("PASS", "POST /api/skills 创建 Skill")
                else:
                    log_result("FAIL", "POST /api/skills 创建 Skill", "响应格式错误")
            else:
                log_result("FAIL", "POST /api/skills 创建 Skill", f"状态码 {resp.status_code}")
        except Exception as e:
            log_result("FAIL", "POST /api/skills 创建 Skill", str(e))

        # 我的上传
        try:
            resp = httpx.get(f"{BASE_URL}/api/skills/uploads/list?page=1", headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if "items" in data and "total" in data:
                    log_result("PASS", "GET /api/skills/uploads/list 我的上传")
                else:
                    log_result("FAIL", "GET /api/skills/uploads/list 我的上传", "响应格式错误")
            else:
                log_result("FAIL", "GET /api/skills/uploads/list 我的上传", f"状态码 {resp.status_code}")
        except Exception as e:
            log_result("FAIL", "GET /api/skills/uploads/list 我的上传", str(e))

        # 管理后台
        try:
            resp = httpx.get(f"{BASE_URL}/api/admin/dashboard", headers=headers, timeout=10)
            if resp.status_code == 200:
                log_result("PASS", "GET /api/admin/dashboard 管理面板")
            else:
                log_result("FAIL", "GET /api/admin/dashboard 管理面板", f"状态码 {resp.status_code}")
        except Exception as e:
            log_result("FAIL", "GET /api/admin/dashboard 管理面板", str(e))

        try:
            resp = httpx.get(f"{BASE_URL}/api/admin/users?page=1", headers=headers, timeout=10)
            if resp.status_code == 200:
                log_result("PASS", "GET /api/admin/users 用户列表")
            else:
                log_result("FAIL", "GET /api/admin/users 用户列表", f"状态码 {resp.status_code}")
        except Exception as e:
            log_result("FAIL", "GET /api/admin/users 用户列表", str(e))

        try:
            resp = httpx.get(f"{BASE_URL}/api/admin/skills/pending?page=1", headers=headers, timeout=10)
            if resp.status_code == 200:
                log_result("PASS", "GET /api/admin/skills/pending 待审核")
            else:
                log_result("FAIL", "GET /api/admin/skills/pending 待审核", f"状态码 {resp.status_code}")
        except Exception as e:
            log_result("FAIL", "GET /api/admin/skills/pending 待审核", str(e))
    else:
        log_result("SKIP", "需要认证的接口", "无 admin token")

    # ---------- 1.9 权限测试 ----------
    print("\n【1.9 权限测试】")
    
    # 无 token 访问收藏
    try:
        resp = httpx.get(f"{BASE_URL}/api/skills/favorites/list?page=1", timeout=10)
        if resp.status_code == 422:
            log_result("PASS", "无 token 访问收藏返回 422")
        else:
            log_result("FAIL", "无 token 访问收藏返回 422", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "无 token 访问收藏返回 422", str(e))

    # 无 token 访问管理
    try:
        resp = httpx.get(f"{BASE_URL}/api/admin/dashboard", timeout=10)
        if resp.status_code == 422:
            log_result("PASS", "无 token 访问管理返回 422")
        else:
            log_result("FAIL", "无 token 访问管理返回 422", f"状态码 {resp.status_code}")
    except Exception as e:
        log_result("FAIL", "无 token 访问管理返回 422", str(e))


# =====================================================================
# Part 2: 小程序前端代码静态检查
# =====================================================================

def test_miniprogram_code():
    """测试小程序前端代码"""
    print(f"\n{CYAN}{'='*60}")
    print(f"Part 2: 小程序前端代码静态检查")
    print(f"目录: {MINIPROGRAM_DIR}")
    print(f"{'='*60}{RESET}\n")

    # ---------- 2.1 app.json 配置 ----------
    print("【2.1 app.json 配置】")
    
    app_json_path = MINIPROGRAM_DIR / "app.json"
    if app_json_path.exists():
        with open(app_json_path, 'r', encoding='utf-8') as f:
            app_json = json.load(f)
        
        # 检查页面列表
        required_pages = [
            "pages/index/index",
            "pages/classify/classify",
            "pages/detail/detail",
            "pages/upload/upload",
            "pages/mine/mine",
            "pages/login/login"
        ]
        actual_pages = app_json.get("pages", [])
        
        missing_pages = [p for p in required_pages if p not in actual_pages]
        if not missing_pages:
            log_result("PASS", "app.json 页面路由完整")
        else:
            log_result("FAIL", "app.json 页面路由完整", f"缺失：{missing_pages}")
        
        # 检查 tabBar
        tabBar = app_json.get("tabBar", {})
        tabBar_list = tabBar.get("list", [])
        required_tabBar = ["pages/index/index", "pages/classify/classify", 
                          "pages/upload/upload", "pages/mine/mine"]
        actual_tabBar = [item["pagePath"] for item in tabBar_list]
        
        missing_tabBar = [p for p in required_tabBar if p not in actual_tabBar]
        if not missing_tabBar:
            log_result("PASS", "app.json tabBar 配置完整")
        else:
            log_result("FAIL", "app.json tabBar 配置完整", f"缺失：{missing_tabBar}")
        
        # 检查 tabBar 图标
        icon_missing = []
        for item in tabBar_list:
            if "iconPath" not in item or "selectedIconPath" not in item:
                icon_missing.append(item.get("pagePath", "unknown"))
        if not icon_missing:
            log_result("PASS", "tabBar 图标配置完整")
        else:
            log_result("FAIL", "tabBar 图标配置完整", f"缺失图标：{icon_missing}")
    else:
        log_result("FAIL", "app.json 配置", "文件不存在")

    # ---------- 2.2 request.js 配置 ----------
    print("\n【2.2 request.js 配置】")
    
    request_js_path = MINIPROGRAM_DIR / "utils" / "request.js"
    if request_js_path.exists():
        with open(request_js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查 USE_CLOUD
        if "const USE_CLOUD = true" in content:
            log_result("PASS", "request.js USE_CLOUD = true (生产模式)")
        elif "const USE_CLOUD = false" in content:
            log_result("FAIL", "request.js USE_CLOUD = true (生产模式)", "当前为 false (开发模式)")
        else:
            log_result("FAIL", "request.js USE_CLOUD 配置", "未找到 USE_CLOUD 变量")
        
        # 检查 CONTAINER_NAME
        if "CONTAINER_NAME = 'flask-p0w8'" in content:
            log_result("PASS", "request.js CONTAINER_NAME 正确")
        else:
            log_result("FAIL", "request.js CONTAINER_NAME 正确", "服务名不匹配")
        
        # 检查 CLOUD_ENV
        if "CLOUD_ENV = 'prod-d6gf8996d0722a6d3'" in content:
            log_result("PASS", "request.js CLOUD_ENV 正确")
        else:
            log_result("FAIL", "request.js CLOUD_ENV 正确", "环境 ID 不匹配")
        
        # 检查请求方法
        required_methods = ["function get(", "function post(", "function put(", "function del("]
        missing_methods = [m for m in required_methods if m not in content]
        if not missing_methods:
            log_result("PASS", "request.js 请求方法完整 (get/post/put/del)")
        else:
            log_result("FAIL", "request.js 请求方法完整", f"缺失：{missing_methods}")
    else:
        log_result("FAIL", "request.js 配置", "文件不存在")

    # ---------- 2.3 页面 API 调用检查 ----------
    print("\n【2.3 页面 API 调用检查】")
    
    # 定义每个页面应该调用的 API
    page_api_map = {
        "pages/index/index.js": [
            "/api/categories",
            "/api/skills?",
            "/api/skills/search/list",
            "/api/settings/ad-switch"
        ],
        "pages/classify/classify.js": [
            "/api/categories",
            "/api/skills?"
        ],
        "pages/detail/detail.js": [
            "/api/skills/",
            "/api/skills/favorites/status",
            "/api/settings/ad-switch",
            "/api/skills/.*?/collect"
        ],
        "pages/upload/upload.js": [
            "/api/categories",
            "/api/skills"
        ],
        "pages/mine/mine.js": [
            "/api/skills/favorites/list",
            "/api/skills/uploads/list"
        ],
        "pages/login/login.js": [
            "/api/auth/login"
        ]
    }
    
    for page_file, expected_apis in page_api_map.items():
        page_path = MINIPROGRAM_DIR / page_file
        if page_path.exists():
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            missing_apis = []
            for api_pattern in expected_apis:
                # 使用正则匹配
                if not re.search(api_pattern, content):
                    missing_apis.append(api_pattern)
            
            if not missing_apis:
                log_result("PASS", f"{page_file} API 调用完整")
            else:
                log_result("FAIL", f"{page_file} API 调用完整", f"缺失：{missing_apis}")
        else:
            log_result("FAIL", f"{page_file} API 调用检查", "文件不存在")

    # ---------- 2.4 页面生命周期检查 ----------
    print("\n【2.4 页面生命周期检查】")
    
    page_lifecycle_map = {
        "pages/index/index.js": ["onLoad", "onPullDownRefresh", "onReachBottom"],
        "pages/classify/classify.js": ["onLoad", "onPullDownRefresh", "onReachBottom"],
        "pages/detail/detail.js": ["onLoad"],
        "pages/upload/upload.js": ["onLoad", "onShow"],
        "pages/mine/mine.js": ["onShow", "onReachBottom"],
        "pages/login/login.js": ["onLoad"]
    }
    
    for page_file, expected_lifecycle in page_lifecycle_map.items():
        page_path = MINIPROGRAM_DIR / page_file
        if page_path.exists():
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            missing_lifecycle = [lc for lc in expected_lifecycle if lc not in content]
            if not missing_lifecycle:
                log_result("PASS", f"{page_file} 生命周期完整")
            else:
                log_result("FAIL", f"{page_file} 生命周期完整", f"缺失：{missing_lifecycle}")
        else:
            log_result("FAIL", f"{page_file} 生命周期检查", "文件不存在")

    # ---------- 2.5 数据绑定检查 ----------
    print("\n【2.5 数据绑定检查】")
    
    # 检查每个页面的 data 定义
    page_data_map = {
        "pages/index/index.js": ["searchKey", "categories", "skills", "page", "hasMore"],
        "pages/classify/classify.js": ["categories", "activeCategory", "skills", "page"],
        "pages/detail/detail.js": ["skill", "mdBlocks", "isFavorited", "loading"],
        "pages/upload/upload.js": ["title", "content", "category", "submitting"],
        "pages/mine/mine.js": ["isLoggedIn", "favorites", "uploads", "activeTab"],
        "pages/login/login.js": ["isLogging"]
    }
    
    for page_file, expected_data in page_data_map.items():
        page_path = MINIPROGRAM_DIR / page_file
        if page_path.exists():
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            missing_data = []
            for d in expected_data:
                # 检查多种格式："key":  'key':  key:
                patterns = [f'"{d}"', f"'{d}'", f"{d}:", f"{d} "]
                if not any(p in content for p in patterns):
                    missing_data.append(d)
            
            if not missing_data:
                log_result("PASS", f"{page_file} 数据定义完整")
            else:
                log_result("FAIL", f"{page_file} 数据定义完整", f"缺失：{missing_data}")
        else:
            log_result("FAIL", f"{page_file} 数据定义检查", "文件不存在")

    # ---------- 2.6 文件完整性检查 ----------
    print("\n【2.6 文件完整性检查】")
    
    required_files = [
        "app.js",
        "app.json",
        "app.wxss",
        "project.config.json",
        "sitemap.json",
        "utils/request.js",
        "utils/logger.js",
        "pages/index/index.js",
        "pages/index/index.json",
        "pages/index/index.wxml",
        "pages/index/index.wxss",
        "pages/classify/classify.js",
        "pages/classify/classify.json",
        "pages/classify/classify.wxml",
        "pages/classify/classify.wxss",
        "pages/detail/detail.js",
        "pages/detail/detail.json",
        "pages/detail/detail.wxml",
        "pages/detail/detail.wxss",
        "pages/upload/upload.js",
        "pages/upload/upload.json",
        "pages/upload/upload.wxml",
        "pages/upload/upload.wxss",
        "pages/mine/mine.js",
        "pages/mine/mine.json",
        "pages/mine/mine.wxml",
        "pages/mine/mine.wxss",
        "pages/login/login.js",
        "pages/login/login.json",
        "pages/login/login.wxml",
        "pages/login/login.wxss"
    ]
    
    missing_files = []
    for file in required_files:
        if not (MINIPROGRAM_DIR / file).exists():
            missing_files.append(file)
    
    if not missing_files:
        log_result("PASS", "小程序文件完整性")
    else:
        log_result("FAIL", "小程序文件完整性", f"缺失：{missing_files}")


# =====================================================================
# 主函数
# =====================================================================

def main():
    print(f"\n{'='*60}")
    print(f"AI Skill 库 - 全栈契约测试")
    print(f"时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    # Part 1: 后端 API 测试
    test_backend_api()
    
    # Part 2: 小程序前端代码检查
    test_miniprogram_code()
    
    # 汇总
    print(f"\n{CYAN}{'='*60}")
    print(f"测试汇总")
    print(f"{'='*60}{RESET}")
    total = stats["passed"] + stats["failed"] + stats["skipped"]
    print(f"总计：{total}")
    print(f"  {GREEN}通过：{stats['passed']}{RESET}")
    print(f"  {RED}失败：{stats['failed']}{RESET}")
    print(f"  {YELLOW}跳过：{stats['skipped']}{RESET}")
    
    if errors:
        print(f"\n{RED}失败项列表:{RESET}")
        for err in errors:
            print(f"  - {err}")
    
    print(f"\n{'='*60}\n")
    
    # 退出码
    sys.exit(0 if stats["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
