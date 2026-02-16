# switchbot_temp_only.py
import os, time, uuid, hmac, base64, hashlib, requests

# ===== SwitchBot設定 =====
# SB_TOKEN   = os.getenv("SWITCHBOT_TOKEN")
# SB_SECRET  = os.getenv("SWITCHBOT_SECRET")
# SB_DEVICE  = os.getenv("SWITCHBOT_DEVICE_ID")
SB_TOKEN = "0e61800e0eac18d5221f3bc1ea208453641572182f714bc24ba957bcb701c99879e947e6743ea7cb68f92deb1df4928b"
SB_SECRET = "0c236172f10b0e376a83323b666f4ccf"
SB_DEVICE  = "C6450D925E8C"
SB_BASE    = "https://api.switch-bot.com/v1.1"

def sb_headers(token: str, secret: str):
    """SwitchBot Cloud API v1.1 の署名ヘッダを生成"""
    t = str(int(time.time() * 1000))
    nonce = str(uuid.uuid4())
    data = (token + t + nonce).encode("utf-8")
    sign = base64.b64encode(
        hmac.new(secret.encode("utf-8"), msg=data, digestmod=hashlib.sha256).digest()
    ).decode()
    return {
        "Authorization": token,
        "sign": sign,
        "t": t,
        "nonce": nonce,
        "Content-Type": "application/json; charset=utf8",
    }

def get_temperature():
    """温度のみ取得"""
    if not (SB_TOKEN and SB_SECRET and SB_DEVICE):
        raise RuntimeError("SWITCHBOT_TOKEN / SECRET / DEVICE_ID が設定されていません。")

    headers = sb_headers(SB_TOKEN, SB_SECRET)
    r = requests.get(f"{SB_BASE}/devices/{SB_DEVICE}/status", headers=headers, timeout=8)
    js = r.json()

    if js.get("statusCode") != 100:
        raise RuntimeError(f"APIエラー: {js}")
    temp = js["body"].get("temperature")
    return temp

def main():
    while True:
        try:
            temp = get_temperature()
            print(time.strftime("[%Y-%m-%d %H:%M:%S]"), f"温度: {temp:.1f}°C")
        except Exception as e:
            print("取得失敗:", e)
#        time.sleep(60)  # 60秒ごとに取得
        time.sleep(2)  # 2秒ごとに取得

if __name__ == "__main__":
    main()
