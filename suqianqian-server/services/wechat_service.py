"""
AI Skill 库 - 微信服务层
封装与微信开放平台的交互逻辑
"""
import httpx
import ssl
from config import settings

# 云托管环境内部代理使用自签名证书，需要跳过 SSL 验证
_ssl_context = ssl.create_default_context()
_ssl_context.check_hostname = False
_ssl_context.verify_mode = ssl.CERT_NONE


async def code2session(code: str) -> dict:
    """
    通过 wx.login() 获取的 code 换取 openid 和 session_key
    接口: https://api.weixin.qq.com/sns/jscode2session
    """
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": settings.WECHAT_APP_ID,
        "secret": settings.WECHAT_APP_SECRET,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(url, params=params)
        data = resp.json()

    if "errcode" in data and data["errcode"] != 0:
        raise Exception(f"微信登录失败: {data.get('errmsg', '未知错误')}")

    return {
        "openid": data["openid"],
        "session_key": data["session_key"],
        "unionid": data.get("unionid"),
    }


async def get_phone_number(code: str) -> str:
    """
    通过 getPhoneNumber 获取的 code 换取用户手机号
    接口: https://api.weixin.qq.com/wxa/business/getuserphonenumber
    """
    # 先获取 access_token
    access_token = await get_access_token()

    url = f"https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={access_token}"
    payload = {"code": code}

    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.post(url, json=payload)
        data = resp.json()

    if data.get("errcode", 0) != 0:
        raise Exception(f"获取手机号失败: {data.get('errmsg', '未知错误')}")

    phone_info = data["phone_info"]
    return phone_info["purePhoneNumber"]


async def get_access_token() -> str:
    """
    获取微信小程序 access_token
    接口: https://api.weixin.qq.com/cgi-bin/token
    """
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": settings.WECHAT_APP_ID,
        "secret": settings.WECHAT_APP_SECRET,
    }
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(url, params=params)
        data = resp.json()

    if "access_token" not in data:
        raise Exception(f"获取 access_token 失败: {data.get('errmsg', '未知错误')}")

    return data["access_token"]
