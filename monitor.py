import json
import os
import urllib.parse
import urllib.request

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

PAGE = "https://www.shop.eva-cosmetics.com/products/clouds-gold-night-out-free-copy"
DATA_URL = PAGE + ".js"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")


def send(text):
    url = "https://api.telegram.org/bot%s/sendMessage" % TOKEN
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    urllib.request.urlopen(url, data=data, timeout=30)


def is_available():
    try:
        return bool(json.loads(fetch(DATA_URL)).get("available"))
    except Exception:
        html = fetch(PAGE)
        return "Sold out" not in html


if is_available():
    send("المنتج اتوفر! 🎉\n" + PAGE)
    print("available")
else:
    print("still sold out")
    if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        send("اختبار: المنتج لسه Sold out، والبوت شغال ✅")
