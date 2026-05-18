#!/usr/bin/env python3
"""
微信公众号发布脚本 (自动发布版)
修改：创建草稿后自动发布，不用手动确认
"""

import os
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
    draw.text((450, 230), datetime.now().strftime("%Y-%m-%d"), font=font_small, fill="#888888", anchor="mm")
    draw.text((450, 300), "AI News Digest", font=font_small, fill="#4ecdc4", anchor="mm")

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


def publish_draft(token, media_id):
    """发布草稿到公众号"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/publish?access_token={token}"
    data = {"media_id": media_id}
    resp = requests.post(
        url,
        data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )
    result = resp.json()
    if result.get("errcode") != 0:
        raise Exception(f"发布失败: {result}")
    return result


def publish_with_content(articles):
    """
    发布已翻译的中文内容到公众号（自动发布）
    articles: [{"title": "标题", "content": "HTML内容", "digest": "摘要", "source_url": "原文链接"}, ...]
    """
    print("=" * 50)
    print("📝 WeChat Publisher Started (Auto-Publish)")
    print(f"Time: {datetime.now()}")
    print(f"Articles: {len(articles)}")
    print("=" * 50)

    if not WECHAT_APP_ID or not WECHAT_APP_SECRET:
        raise Exception("WeChat not configured")

    print("\n🔑 Getting access token...")
    token = get_access_token()

    print("📤 Uploading cover...")
    thumb_id = upload_cover_image(token)

    print("📝 Creating draft...")
    wechat_articles = []
    for i, article in enumerate(articles):
        wechat_article = {
            "title": article.get("title", ""),
            "author": "Veray AI",
            "content": article.get("content", ""),
            "digest": article.get("digest", article.get("title", "")),
            "thumb_media_id": thumb_id,
            "content_source_url": article.get("source_url", "https://veray.ai"),
        }
        wechat_articles.append(wechat_article)

    # 创建草稿
    media_id = create_draft(token, wechat_articles)
    print(f"✅ Draft created: {media_id}")

    # ====== 新增：自动发布 ======
    print("🚀 Publishing to official account...")
    result = publish_draft(token, media_id)
    print(f"✅ Published successfully! msg_id: {result.get('msg_id')}")
    # ====== 自动发布完成 ======

    return {"media_id": media_id, "article_count": len(articles), "published": True}


def publish_with_content_draft_only(articles):
    """
    仅创建草稿（不发布）- 保留原功能
    """
    print("=" * 50)
    print("📝 WeChat Publisher Started (Draft Only)")
    print(f"Time: {datetime.now()}")
    print(f"Articles: {len(articles)}")
    print("=" * 50)

    if not WECHAT_APP_ID or not WECHAT_APP_SECRET:
        raise Exception("WeChat not configured")

    print("\n🔑 Getting access token...")
    token = get_access_token()

    print("📤 Uploading cover...")
    thumb_id = upload_cover_image(token)

    print("📝 Creating draft...")
    wechat_articles = []
    for i, article in enumerate(articles):
        wechat_article = {
            "title": article.get("title", ""),
            "author": "Veray AI",
            "content": article.get("content", ""),
            "digest": article.get("digest", article.get("title", "")),
            "thumb_media_id": thumb_id,
            "content_source_url": article.get("source_url", "https://veray.ai"),
        }
        wechat_articles.append(wechat_article)

    media_id = create_draft(token, wechat_articles)
    print(f"✅ Draft created: {media_id}")
    return {"media_id": media_id, "article_count": len(articles)}
