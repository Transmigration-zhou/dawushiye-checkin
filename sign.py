"""
大物是也微信小程序自动签到脚本

Usage:
    python sign.py --token <your_jwt_token>
"""

import argparse
import json
import os
import sys
from datetime import datetime

import requests

# ── 接口配置 ──────────────────────────────────────────────
BASE_URL = "https://api.dawushiye.com"
SIGN_URL = f"{BASE_URL}/api/MarketingWechat/Sign/MiniUserSign"
QUERY_URL = f"{BASE_URL}/api/MarketingWechat/Sign/GetMiniUserSignData"

# ── 请求头模板（模拟微信小程序环境）─────────────────────────
BASE_HEADERS = {
    "Host": "api.dawushiye.com",
    "Connection": "keep-alive",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/132.0.0.0 Safari/537.36 "
        "MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI "
        "MiniProgramEnv/Mac MacWechat/WMPF "
        "MacWechat/3.8.7(0x13080712) "
        "UnifiedPCMacWechat(0xf2641701) XWEB/18788"
    ),
    "xweb_xhr": "1",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/wx9d7354501dec9fe8/21/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def build_headers(token: str) -> dict:
    """构造带认证的请求头。"""
    headers = BASE_HEADERS.copy()
    headers["Authorization"] = token
    return headers


def query_sign_data(token: str) -> dict | None:
    """查询当前签到状态。"""
    try:
        resp = requests.post(
            QUERY_URL,
            headers=build_headers(token),
            data="null",
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"[ERROR] 查询签到状态失败: {e}")
        return None


def do_sign(token: str) -> dict | None:
    """执行签到。"""
    try:
        resp = requests.post(
            SIGN_URL,
            headers=build_headers(token),
            data="null",
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"[ERROR] 签到请求失败: {e}")
        return None


def run(token: str):
    """主流程：查询状态 → 签到 → 输出结果。"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*50}")
    print(f"  大物是也 自动签到  |  {now}")
    print(f"{'='*50}")

    # 1. 查询当前签到数据
    print("\n[1/2] 查询签到状态...")
    query_result = query_sign_data(token)
    if query_result:
        print(f"      响应: {json.dumps(query_result, ensure_ascii=False)}")

    # 2. 执行签到
    print("\n[2/2] 执行签到...")
    sign_result = do_sign(token)

    if sign_result is None:
        print("\n[FAIL] 签到失败，请检查网络或 token 是否过期")
        sys.exit(1)

    print(f"      响应: {json.dumps(sign_result, ensure_ascii=False)}")

    code = (
        sign_result.get("resultCode")
        if sign_result.get("resultCode") is not None
        else sign_result.get("code") or sign_result.get("Code")
    )
    msg = (
        sign_result.get("errorMessage")
        or sign_result.get("msg")
        or sign_result.get("message")
        or sign_result.get("Message")
        or ""
    )
    integral = (sign_result.get("data") or {}).get("integral")

    if code in (0, 200, "0", "200", True, "success"):
        reward = f"，获得 {integral} 积分" if integral is not None else ""
        print(f"\n[OK] 签到成功！{reward} {msg}")
    elif msg and "已签到" in msg:
        print(f"\n[OK] 今日已签到，无需重复签到")
    else:
        print(f"\n[FAIL] 签到失败: code={code}, msg={msg}")
        sys.exit(1)

    print(f"\n{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(description="大物是也微信小程序自动签到")
    parser.add_argument("--token", "-t", help="JWT token（覆盖 DAWU_TOKEN 环境变量）")
    args = parser.parse_args()

    token = args.token or os.getenv("DAWU_TOKEN", "").strip()
    if not token:
        print("[ERROR] 未提供 token，请设置环境变量 DAWU_TOKEN 或使用 --token 参数")
        sys.exit(1)
    run(token)


if __name__ == "__main__":
    main()
