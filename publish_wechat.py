#!/usr/bin/env python3
"""
微信公众号发布脚本
用于 Railway 部署
支持接收已翻译的中文内容并发布到公众号草稿箱
"""

import os
import sys
import json
import sqlite3
import time
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import tempfile

DATABASE_URL = os.environ.get("DATABASE_URL", "data/news.db")
WECHAT_APP_ID = os.environ.get("WECHAT_APP_ID", "")
WECHAT_APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "")


def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


def get_access_token():
    """获取微信 access_token"""
    if not WECHAT_APP_ID or not WECHAT_APP_SECRET:
        raise Exception("WeChat APP_ID or APP_SECRET not configured")

    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}"
    resp = requests.get(url)
    data = resp.json()
    if "access_token" in data:
        return data["access_token"]
    raise Exception(f"获取token失败: {data}")


def upload_qrcode_image(token):
    """上传二维码图片到微信素材库"""
    qrcode_path = os.path.join(os.path.dirname(__file__), "grepAI_qrcode.png")
    if not os.path.exists(qrcode_path):
        print(f"QR code not found: {qrcode_path}")
        return None

    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    with open(qrcode_path, "rb") as f:
        files = {"media": f}
        resp = requests.post(url, files=files, timeout=30)
        result = resp.json()
        if "media_id" in result:
            return result["media_id"]
        print(f"上传二维码失败: {result}")
        return None


def upload_cover_image(token):
    """创建并上传封面图片"""
    img = Image.new("RGB", (900, 383), color="#1a1a3e")
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 50)
        font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 20)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((450, 150), "AI Daily", font=font_large, fill="#ffffff", anchor="mm")
    draw.text(
        (450, 230),
        datetime.now().strftime("%Y-%m-%d"),
        font=font_small,
        fill="#888888",
        anchor="mm",
    )
    draw.text(
        (450, 300), "AI News Digest", font=font_small, fill="#4ecdc4", anchor="mm"
    )

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        img.save(f.name, "JPEG", quality=95)
        temp_path = f.name

    try:
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
        with open(temp_path, "rb") as f:
            files = {"media": f}
            resp = requests.post(url, files=files, timeout=30)
            result = resp.json()
            if "media_id" in result:
                return result["media_id"]
            raise Exception(f"上传封面失败: {result}")
    finally:
        os.unlink(temp_path)


def create_draft(token, articles):
    """创建草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    data = {"articles": articles}
    resp = requests.post(
        url,
        data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )
    result = resp.json()
    if "errcode" in result and result["errcode"] != 0:
        raise Exception(f"创建草稿失败: {result}")
    return result.get("media_id", "")


def publish_with_content(articles):
    """
    发布已翻译的中文内容到公众号草稿箱
    articles: [
        {
            "title": "标题",
            "content": "HTML内容",
            "digest": "摘要",
            "source_url": "原文链接"
        },
        ...
    ]
    """
    print("=" * 50)
    print("📝 WeChat Publisher Started")
    print(f"Time: {datetime.now()}")
    print(f"Articles: {len(articles)}")
    print("=" * 50)

    if not WECHAT_APP_ID or not WECHAT_APP_SECRET:
        raise Exception("WeChat not configured")

    print("\n🔑 Getting access token...")
    token = get_access_token()

    print("📤 Uploading cover...")
    thumb_id = upload_cover_image(token)

    print("📤 Uploading QR code...")
    qrcode_media_id = upload_qrcode_image(token)

    print("📝 Creating draft...")
    wechat_articles = []
    for i, article in enumerate(articles):
        content = article.get("content", "")
        if qrcode_media_id:
            qrcode_html = f"""
<p style="text-align: center; margin-top: 30px;">
    <img data-src="{qrcode_media_id}" 
         style="width: 200px; height: auto; border-radius: 8px;" 
         alt="扫码关注">
</p>
<p style="text-align: center; margin-top: 10px; font-size: 13px; color: #666;">
    📱 扫码搜索「grepAI」<br>
    每天早上8点自动送达
</p>
"""
            content += qrcode_html

        wechat_article = {
            "title": article.get("title", ""),
            "author": "Veray AI",
            "content": content,
            "digest": article.get("digest", article.get("title", "")),
            "thumb_media_id": thumb_id,
            "content_source_url": article.get("source_url", "https://veray.ai"),
        }
        wechat_articles.append(wechat_article)

    media_id = create_draft(token, wechat_articles)

    print(f"✅ Draft created: {media_id}")
    return True


def generate_article_content(news_data, qrcode_media_id=None):
    """生成文章 HTML 内容"""
    date_str = datetime.now().strftime("%Y.%m.%d")
    weekday_map = {
        0: "星期一",
        1: "星期二",
        2: "星期三",
        3: "星期四",
        4: "星期五",
        5: "星期六",
        6: "星期日",
    }
    weekday = weekday_map[datetime.now().weekday()]
    total_count = sum(len(items) for items in news_data.values())

    html = f"""
<p style="text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 5px;">{date_str} 全球AI科技早报</p>
<p style="text-align: center; color: #888; font-size: 12px; margin-bottom: 15px;">{total_count}条精选速览</p>
<p style="text-align: center; font-size: 16px; font-weight: bold; margin: 20px 0 10px;">✨ 今日播报｜{date_str} {weekday}</p>
<p style="background: #f0f0f0; padding: 12px; border-radius: 8px; margin: 15px 0;">Hello 各位科技人～ 今日精选全球AI科技资讯，一键速览！</p>
"""

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

    for source, items in news_data.items():
        if not items:
            continue
        icon = icons.get(source, "📰")
        name = source_names.get(source, source)
        html += f'<p style="font-size: 18px; font-weight: bold; margin: 25px 0 12px;">{icon} {name}</p>'

        for i, item in enumerate(items[:5], 1):
            title = item.get("title_zh") or item.get("title", "")
            url = item.get("url", "")
            score = item.get("score", 0)
            html += f'<p><strong>{i}. {title}</strong> <span style="color:#888;">❤️{score}</span></p>'
            html += f'<p style="color:#1976d2;font-size:11px;">🔗 {url}</p>'

    html += '<p style="background:#f5f5f5;padding:12px;border-radius:8px;margin:20px 0;">📌 关注我们，每日获取 AI 科技前沿资讯！</p>'

    qrcode_html = ""
    if qrcode_media_id:
        qrcode_html = f"""
<p style="text-align: center; margin-top: 30px;">
    <img data-src="{qrcode_media_id}" 
         style="width: 200px; height: auto; border-radius: 8px;" 
         alt="扫码关注">
</p>
"""
    qrcode_html += """
<p style="text-align: center; margin-top: 10px; font-size: 13px; color: #666;">
    📱 扫码搜索「grepAI」<br>
    每天早上8点自动送达
</p>
"""
    html += qrcode_html

    return html


if __name__ == "__main__":
    success = publish()
    sys.exit(0 if success else 1)
