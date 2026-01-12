from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# LẤY BIẾN MÔI TRƯỜNG (Render sẽ cấp)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/")
def home():
    return "API Telegram Bot đang chạy OK"

@app.route("/send", methods=["POST"])
def send():
    data = request.json or {}

    time_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    text = (
        "📩 *DỮ LIỆU MỚI*\n\n"
        f"👤 *Tên:* {data.get('name', 'Không có')}\n"
        f"📝 *Nội dung:* {data.get('message', 'Không có')}\n\n"
        f"⏰ *Thời gian:* {time_str}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }
    )

    return jsonify({"status": "ok"})

# BẮT BUỘC CÓ ĐOẠN NÀY KHI DEPLOY
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
