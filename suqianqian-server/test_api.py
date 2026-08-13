"""
AI Skill 库 - API 契约测试
测试所有接口的请求/响应格式是否符合约定
"""
import httpx
import json
import sys

BASE_URL = "https://flask-p0w8-296442-11-1453433457.sh.run.tcloudbase.com"

# 颜色输出
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

passed = 0
failed = 0
skipped = 0
errors = []


def check(name, method, path, expected_status=200, check_fn=None, data=None, headers=None, skip=False):
    global passed, failed, skipped
    if skip:
        print(f"  {YELLOW}⊘ SKIP{RESET}  {method:6s} {path}  — {name}")
        skipped += 1
        return None

    url = f"{BASE_URL}{path}"
    try:
        if method == "GET":
            resp = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        elif method == "POST":
            resp = httpx.post(url, json=data, headers=headers, timeout=10, follow_redirects=True)
        elif method == "PUT":
            resp = httpx.put(url, json=data, headers=headers, timeout=10, follow_redirects=True)
        else:
            resp = httpx.request(method, url, json=data, headers=headers, timeout=10)

        ok = resp.status_code == expected_status
        if check_fn and ok:
            try:
                ok = check_fn(resp.json())
            except Exception as e:
                ok = False
                print(f"    检查函数异常: {e}")

        if ok:
            print(f"  {GREEN}✓ PASS{RESET}  {method:6s} {path}  → {resp.status_code}  [{name}]")
            passed += 1
        else:
            print(f"  {RED}✗ FAIL{RESET}  {method:6s} {path}  → {resp.status_code} (期望 {expected_status})  [{name}]")
            try:
                body = resp.text[:200]
                print(f"    响应: {body}")
            except:
                pass
            failed += 1
            errors.append(f"{method} {path}: {resp.status_code}")
        return resp.json() if resp.status_code < 400 else None
    except Exception as e:
        print(f"  {RED}✗ FAIL{RESET}  {method:6s} {path}  — 请求异常: {e}  [{name}]")
        failed += 1
        errors.append(f"{method} {path}: {e}")
        return None


# ==================== 测试开始 ====================

print(f"\n{'='*60}")
print(f"AI Skill 库 API 契约测试")
print(f"目标: {BASE_URL}")
print(f"{'='*60}\n")

# ---------- 1. 基础接口 ----------
print("【1. 基础接口】")
check("根路径", "GET", "/",
      check_fn=lambda d: "message" in d and "version" in d)

check("健康检查", "GET", "/health",
      check_fn=lambda d: d.get("status") == "ok")

# ---------- 2. 分类接口 ----------
print("\n【2. 分类接口】")
check("获取分类树", "GET", "/api/categories",
      check_fn=lambda d: "categories" in d and isinstance(d["categories"], list))

# ---------- 3. Skill 列表 ----------
print("\n【3. Skill 列表】")
check("默认列表(page=1)", "GET", "/api/skills?page=1&page_size=5",
      check_fn=lambda d: "items" in d and "total" in d and "page" in d
                       and isinstance(d["items"], list) and len(d["items"]) <= 5)

check("按分类筛选", "GET", "/api/skills?category=通用AI能力&page_size=3",
      check_fn=lambda d: all(s["category"] == "通用AI能力" for s in d.get("items", [])))

check("分页参数", "GET", "/api/skills?page=2&page_size=3",
      check_fn=lambda d: d.get("page") == 2)

# ---------- 4. Skill 详情 ----------
print("\n【4. Skill 详情】")
# 先获取一个有效 ID
list_resp = check("获取首个Skill ID", "GET", "/api/skills?page=1&page_size=1")
first_id = None
if list_resp and list_resp.get("items"):
    first_id = list_resp["items"][0]["id"]

if first_id:
    check(f"Skill详情(id={first_id})", "GET", f"/api/skills/{first_id}",
          check_fn=lambda d: "id" in d and "title" in d and "content" in d
                           and "tags" in d and "fit_tools" in d)

    check("不存在的Skill", "GET", "/api/skills/99999", expected_status=404)
else:
    print(f"  {YELLOW} SKIP{RESET}  无有效 Skill ID，跳过详情测试")
    skipped += 2

# ---------- 5. 搜索接口 ----------
print("\n【5. 搜索接口】")
check("搜索关键词", "GET", "/api/skills/search/list?keyword=代码&page=1&page_size=5",
      check_fn=lambda d: "items" in d and "keyword" in d and d["keyword"] == "代码")

check("搜索无结果", "GET", "/api/skills/search/list?keyword=xyznotfound&page=1",
      check_fn=lambda d: d.get("total", -1) == 0)

check("搜索空关键词(400)", "GET", "/api/skills/search/list?keyword=&page=1", expected_status=422)

# ---------- 6. 设置接口 ----------
print("\n【6. 设置接口】")
check("广告开关", "GET", "/api/settings/ad-switch",
      check_fn=lambda d: "ad_enabled" in d)

# ---------- 7. 需要登录的接口 ----------
print("\n【7. 登录相关接口（需要 token）】")

# 微信登录需要真实 code，这里测试接口格式
check("微信登录(无效code)", "POST", "/api/auth/login",
      data={"code": "invalid_code_test"}, expected_status=400)

check("管理员登录(错误密码)", "POST", "/api/auth/admin-login",
      data={"password": "wrong_password"}, expected_status=401)

# 用管理员登录获取 token（如果密码正确）
admin_token = None
login_resp = check("管理员登录", "POST", "/api/auth/admin-login",
                   data={"password": "admin123456"},
                   skip=False)
if login_resp and login_resp.get("token"):
    admin_token = login_resp["token"]
    print(f"    → 获取到 admin token: {admin_token[:20]}...")
else:
    print(f"    → 未获取到 token，后续需要认证的接口将跳过")

auth_headers = {"Authorization": f"Bearer {admin_token}"} if admin_token else {}

# ---------- 8. 收藏接口（需登录）----------
print("\n【8. 收藏接口】")
if admin_token and first_id:
    check(f"收藏Skill(id={first_id})", "POST", f"/api/skills/{first_id}/collect",
          headers=auth_headers,
          check_fn=lambda d: "collected" in d)

    check(f"收藏状态(id={first_id})", "GET", f"/api/skills/favorites/status?skill_id={first_id}",
          headers=auth_headers,
          check_fn=lambda d: "is_favorited" in d)

    check("收藏列表", "GET", "/api/skills/favorites/list?page=1",
          headers=auth_headers,
          check_fn=lambda d: "items" in d and "total" in d)

    # 取消收藏
    check(f"取消收藏(id={first_id})", "POST", f"/api/skills/{first_id}/collect",
          headers=auth_headers,
          check_fn=lambda d: d.get("collected") == False)
else:
    print(f"  {YELLOW}⊘ SKIP{RESET}  无 token，跳过收藏测试")
    skipped += 4

# ---------- 9. 上传接口（需登录）----------
print("\n【9. 上传/我的接口】")
if admin_token:
    check("创建Skill", "POST", "/api/skills",
          headers=auth_headers,
          data={
              "title": "契约测试Skill",
              "desc": "自动化测试创建",
              "content": "# 测试内容\n这是契约测试自动创建的Skill",
              "category": "通用AI能力",
              "tags": ["测试"],
              "fit_tools": ["Ollama"],
          },
          check_fn=lambda d: "id" in d and "message" in d)

    check("我的上传列表", "GET", "/api/skills/uploads/list?page=1",
          headers=auth_headers,
          check_fn=lambda d: "items" in d and "total" in d)
else:
    print(f"  {YELLOW}⊘ SKIP{RESET}  无 token，跳过上传测试")
    skipped += 2

# ---------- 10. 管理接口（需管理员）----------
print("\n【10. 管理后台接口】")
if admin_token:
    check("管理面板", "GET", "/api/admin/dashboard",
          headers=auth_headers,
          check_fn=lambda d: "total_skills" in d or "total_users" in d or "pending_count" in d)

    check("用户列表", "GET", "/api/admin/users?page=1",
          headers=auth_headers,
          check_fn=lambda d: "items" in d)

    check("待审核列表", "GET", "/api/admin/pending-skills",
          headers=auth_headers,
          check_fn=lambda d: "items" in d)

    check("全部Skill(含待审核)", "GET", "/api/admin/all-skills?page=1",
          headers=auth_headers,
          check_fn=lambda d: "items" in d)

    check("获取设置", "GET", "/api/admin/settings",
          headers=auth_headers,
          check_fn=lambda d: isinstance(d, list) or "settings" in d)

    check("更新设置", "PUT", "/api/admin/settings",
          headers=auth_headers,
          data={"key": "ad_enabled", "value": "false"},
          check_fn=lambda d: "message" in d)
else:
    print(f"  {YELLOW}⊘ SKIP{RESET}  无 admin token，跳过管理接口测试")
    skipped += 6

# ---------- 11. 无权限测试 ----------
print("\n【11. 权限测试】")
check("无token访问收藏", "GET", "/api/skills/favorites/list?page=1", expected_status=422)
check("无token访问管理", "GET", "/api/admin/dashboard", expected_status=422)

# ---------- 汇总 ----------
print(f"\n{'='*60}")
total = passed + failed + skipped
print(f"总计: {total}  |  {GREEN}通过: {passed}{RESET}  |  {RED}失败: {failed}{RESET}  |  {YELLOW}跳过: {skipped}{RESET}")
if errors:
    print(f"\n失败项:")
    for e in errors:
        print(f"  - {e}")
print(f"{'='*60}\n")

sys.exit(0 if failed == 0 else 1)
