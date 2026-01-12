from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime
import base64
import json
import random

app = Flask(__name__)

# ===== CONFIG =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
API_KEY = os.environ.get("API_KEY")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# ===== TOOLS =====
def send_telegram(chat_id, text):
    requests.post(TELEGRAM_API, json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    })

def random_username(name):
    return name.lower().replace(" ", "") + str(random.randint(100,999))

def random_password():
    return base64.b64encode(os.urandom(9)).decode()

def random_stk():
    return "".join(str(random.randint(0,9)) for _ in range(12))

def encode_base64(data):
    return base64.b64encode(json.dumps(data).encode()).decode()

# ===== ROOT =====
@app.route("/")
def home():
    return "API Telegram Bot đang chạy OK"

# ===== RECEIVE API =====
@app.route("/send", methods=["POST"])
def receive():
    if request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    name = data.get("name", "demo")

    payload = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": random_username(name),
        "password": random_password(),
        "stk": random_stk()
    }

    encoded = encode_base64(payload)
    send_telegram(CHAT_ID, f"📦 *DATA DEMO*\\n`{encoded}`")

    return jsonify({"ok": True})

# ===== TELEGRAM WEBHOOK =====
@app.route("/telegram", methods=["POST"])
def telegram():
    data = request.get_json(silent=True) or {}

    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    if text == "/start":
        send_telegram(chat_id, "🤖 Bot đã sẵn sàng")

    return "ok"

# ===== RUN =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
