import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, render_template_string, request
import requests

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "news.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT,
            content TEXT,
            summary TEXT,
            score INTEGER DEFAULT 0,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title_zh TEXT,
            summary_zh TEXT,
            icon TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 日报 | {{ date }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; color: #333; line-height: 1.6; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; background: linear-gradient(135deg, #1a1a3e 0%, #2d2d5a 100%); color: white; padding: 40px 20px; border-radius: 16px; margin-bottom: 24px; }
        .header h1 { font-size: 28px; font-weight: 700; margin-bottom: 8px; }
        .header .date { opacity: 0.8; font-size: 14px; }
        .stats { display: flex; justify-content: center; gap: 20px; margin-top: 16px; }
        .stats span { background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 12px; }
        .section { background: white; border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .section-title { font-size: 18px; font-weight: 600; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #eee; display: flex; align-items: center; gap: 8px; }
        .news-item { padding: 12px 0; border-bottom: 1px solid #f5f5f5; }
        .news-item:last-child { border-bottom: none; }
        .news-title { font-size: 15px; font-weight: 500; color: #1a1a1a; text-decoration: none; display: block; margin-bottom: 6px; }
        .news-title:hover { color: #1976d2; }
        .news-meta { display: flex; align-items: center; gap: 12px; font-size: 12px; color: #888; }
        .news-score { color: #ff6b6b; }
        .news-summary { font-size: 13px; color: #666; margin-top: 6px; }
        .footer { text-align: center; padding: 30px; color: #999; font-size: 12px; }
        .footer a { color: #1976d2; text-decoration: none; }
        @media (max-width: 600px) { .container { padding: 12px; } .header { padding: 30px 16px; } .header h1 { font-size: 22px; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI 日报</h1>
            <div class="date">{{ date }} · {{ weekday }}</div>
            <div class="stats">
                <span>📰 {{ total }} 条精选</span>
            </div>
        </div>
        
        {% for source, items in news.items() %}
        <div class="section">
            <div class="section-title">{{ icons.get(source, '📰') }} {{ source_names.get(source, source) }}</div>
            {% for item in items %}
            <div class="news-item">
                <a href="{{ item.url or '#' }}" target="_blank" class="news-title">{{ item.title_zh or item.title }}</a>
                <div class="news-meta">
                    {% if item.score %}
                    <span class="news-score">❤️ {{ item.score }}</span>
                    {% endif %}
                </div>
                {% if item.summary_zh or item.summary %}
                <div class="news-summary">{{ item.summary_zh or item.summary }}</div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endfor %}
        
        <div class="footer">
            <p>由 <a href="https://veray.ai">Veray AI</a> 自动生成</p>
            <p>每日 8:00 自动更新</p>
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    date = request.args.get("date") or datetime.now().strftime("%Y-%m-%d")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM news WHERE date LIKE ? ORDER BY score DESC", (date + "%",)
    )
    rows = cursor.fetchall()
    conn.close()

    news_data = {}
    for row in rows:
        source = row["source"]
        if source not in news_data:
            news_data[source] = []
        news_data[source].append(dict(row))

    weekday_map = {
        "0": "周一",
        "1": "周二",
        "2": "周三",
        "3": "周四",
        "4": "周五",
        "5": "周六",
        "6": "周日",
    }
    weekday = weekday_map.get(str(datetime.now().weekday()), "")

    icons = {
        "HackerNews": "🔥",
        "OpenAI": "🧠",
        "ProductHunt": "🆕",
        "TechCrunch": "🚀",
        "SubStack": "📚",
    }
    source_names = {
        "HackerNews": "Hacker News 热门",
        "OpenAI": "OpenAI 最新动态",
        "TechCrunch": "TechCrunch 科技资讯",
    }

    total = sum(len(items) for items in news_data.values())

    return render_template_string(
        HTML_TEMPLATE,
        date=date,
        weekday=weekday,
        news=news_data,
        total=total,
        icons=icons,
        source_names=source_names,
    )


@app.route("/api/news")
def api_news():
    date = request.args.get("date") or datetime.now().strftime("%Y-%m-%d")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM news WHERE date LIKE ? ORDER BY score DESC", (date + "%",)
    )
    rows = cursor.fetchall()
    conn.close()

    news_data = {}
    for row in rows:
        source = row["source"]
        if source not in news_data:
            news_data[source] = []
        news_data[source].append(dict(row))

    return jsonify({"date": date, "news": news_data})


@app.route("/api/fetch", methods=["GET"])
def api_fetch():
    """抓取当天AI新闻，返回英文JSON"""
    from fetch_news import main as fetch_main, get_news_json

    date = request.args.get("date") or datetime.now().strftime("%Y-%m-%d")

    print(f"🚀 Fetching AI News for {date}")

    try:
        fetch_main(date)
    except Exception as e:
        print(f"Fetch error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    news_json = get_news_json(date)

    return jsonify({"status": "ok", **news_json})


@app.route("/api/publish_wechat", methods=["POST"])
def api_publish_wechat():
    """接收已翻译的中文内容，发布到微信公众号草稿箱"""
    from publish_wechat import publish_with_content

    try:
        data = request.get_json()
        articles = data.get("articles", [])

        if not articles:
            return jsonify({"status": "error", "message": "No articles provided"}), 400

        result = publish_with_content(articles)
        return jsonify({"status": "ok", **result})

    except Exception as e:
        print(f"Publish error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/news/dates")
def api_dates():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT date FROM news ORDER BY date DESC LIMIT 30")
    dates = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(dates)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ai-news"})


@app.route("/api/upload_qrcode", methods=["POST"])
def api_upload_qrcode():
    """上传二维码图片到微信素材库，返回media_id"""
    from publish_wechat import get_access_token
    import requests
    
    try:
        data = request.get_json()
        image_url = data.get("image_url")
        
        if not image_url:
            return jsonify({"status": "error", "message": "No image_url provided"}), 400
        
        # Download image
        resp = requests.get(image_url, timeout=30)
        if resp.status_code != 200:
            return jsonify({"status": "error", "message": "Failed to download image"}), 400
        
        # Get token and upload
        token = get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
        
        from io import BytesIO
        files = {"media": ("qrcode.png", BytesIO(resp.content), "image/png")}
        upload_resp = requests.post(url, files=files, timeout=30)
        result = upload_resp.json()
        
        if "media_id" in result:
            return jsonify({"status": "ok", "media_id": result["media_id"]})
        else:
            return jsonify({"status": "error", "message": result}), 400
            
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
