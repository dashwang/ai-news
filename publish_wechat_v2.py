#!/usr/bin/env python3
"""
微信公众号发布脚本
用于 Railway 部署
支持：
1. 自定义封面图片（通过URL）
2. 自动生成封面
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
import io

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


def download_image(url):
    """从URL下载图片"""
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            return resp.content
    except Exception as e:
        print(f"下载图片失败: {e}")
    return None


def upload_image_from_url(token, image_url):
    """从URL下载图片并上传到微信素材库"""
    print(f"📥 下载图片: {image_url}")
    image_data = download_image(image_url)
    
    if not image_data:
        # 如果下载失败，使用默认封面
        return None
    
    # 下载成功，上传到微信
    try:
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
        files = {"media": ("cover.jpg", image_data, "image/jpeg")}
        resp = requests.post(url, files=files, timeout=30)
        result = resp.json()
        if "media_id" in result:
            print(f"✅ 图片上传成功: {result['media_id']}")
            return result["media_id"]
        else:
            print(f"⚠️ 图片上传失败: {result}")
    except Exception as e:
        print(f"⚠️ 上传异常: {e}")
    
    return None


def create_default_cover(token):
    """创建默认封面图片"""
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

    # 保存到内存
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="JPEG", quality=95)
    img_buffer.seek(0)

    try:
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
        files = {"media": ("cover.jpg", img_buffer, "image/jpeg")}
        resp = requests.post(url, files=files, timeout=30)
        result = resp.json()
        if "media_id" in result:
            return result["media_id"]
        raise Exception(f"上传封面失败: {result}")
    except Exception as e:
        print(f"默认封面上传失败: {e}")
    return None


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
            "source_url": "原文链接",
            "cover_url": "封面图片URL（可选）"
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

    # 获取封面图片（使用第一篇文章的cover_url）
    thumb_id = None
    cover_url = articles[0].get("cover_url") if articles else None
    if cover_url:
        thumb_id = upload_image_from_url(token, cover_url)
    
    # 如果没有自定义封面，使用默认封面
    if not thumb_id:
        print("📤 使用默认封面...")
        thumb_id = create_default_cover(token)

    print("📝 Creating draft...")
    wechat_articles = []
    for i, article in enumerate(articles):
        wechat_article = {
            "title": article.get("title", ""),
            "author": "grepAI",
            "content": article.get("content", ""),
            "digest": article.get("digest", article.get("title", "")),
            "thumb_media_id": thumb_id,
            "content_source_url": article.get("source_url", "https://postiz.com"),
        }
        wechat_articles.append(wechat_article)

    media_id = create_draft(token, wechat_articles)

    print(f"✅ Draft created: {media_id}")
    return {"media_id": media_id, "article_count": len(articles)}


if __name__ == "__main__":
    # 测试发布
    test_articles = [
        {
            "title": "测试文章",
            "content": "<p>测试内容</p>",
            "digest": "测试摘要",
            "source_url": "https://example.com",
            "cover_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=900"
        }
    ]
    result = publish_with_content(test_articles)
    print(result)
