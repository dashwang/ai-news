#!/usr/bin/env python3
"""
微信公众号配图生成器
根据标题动态生成封面图片，直接上传到微信素材库
"""

import os
import sys
import json
import requests
from PIL import Image, ImageDraw, ImageFont
import io

WECHAT_APP_ID = os.environ.get("WECHAT_APP_ID", "")
WECHAT_APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "")


def get_access_token():
    """获取微信 access_token"""
    if not WECHAT_APP_ID or not WECHAT_APP_SECRET:
        raise Exception("请设置 WECHAT_APP_ID 和 WECHAT_APP_SECRET 环境变量")
    
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}"
    resp = requests.get(url)
    data = resp.json()
    if "access_token" in data:
        return data["access_token"]
    raise Exception(f"获取token失败: {data}")


def generate_cover_image(title, subtitle=""):
    """生成封面图片（900x383像素）"""
    # 创建图片
    img = Image.new("RGB", (900, 383), color="#1a1a3e")
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体
    try:
        # Linux 路径
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        try:
            # Mac 路径
            font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 42)
            font_subtitle = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
            font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 18)
        except:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # 标题（处理长标题）
    display_title = title[:30] + "..." if len(title) > 30 else title
    
    # 绘制标题
    draw.text((450, 150), display_title, font=font_title, fill="#ffffff", anchor="mm")
    
    # 绘制副标题
    if subtitle:
        draw.text((450, 220), subtitle, font=font_subtitle, fill="#ff6600", anchor="mm")
    
    # 绘制底部信息
    draw.text((450, 320), "TrustMRR人物志", font=font_small, fill="#4ecdc4", anchor="mm")
    draw.text((450, 350), "扫码关注 · grepAI", font=font_small, fill="#888888", anchor="mm")
    
    return img


def upload_image(token, image_data, filename="cover.jpg"):
    """上传图片到微信素材库"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    files = {"media": (filename, image_data, "image/jpeg")}
    resp = requests.post(url, files=files, timeout=60)
    result = resp.json()
    
    if "media_id" in result:
        return result["media_id"]
    raise Exception(f"上传失败: {result}")


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


def publish_article(title, content, digest, source_url, subtitle=""):
    """发布文章（带动态生成的封面）"""
    print(f"📝 发布文章: {title}")
    
    # 1. 获取 token
    token = get_access_token()
    print("✅ 获取token成功")
    
    # 2. 生成封面图片
    print("🎨 生成封面图片...")
    img = generate_cover_image(title, subtitle)
    
    # 3. 转换为 JPEG
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="JPEG", quality=90)
    img_buffer.seek(0)
    image_data = img_buffer.getvalue()
    print(f"✅ 图片生成成功: {len(image_data)} bytes")
    
    # 4. 上传封面
    thumb_id = upload_image(token, image_data, "cover.jpg")
    print(f"✅ 封面上传成功: {thumb_id}")
    
    # 5. 创建草稿
    article = {
        "title": title,
        "author": "grepAI",
        "content": content,
        "digest": digest,
        "thumb_media_id": thumb_id,
        "content_source_url": source_url,
    }
    
    media_id = create_draft(token, [article])
    print(f"✅ 草稿创建成功: {media_id}")
    
    return {"media_id": media_id, "thumb_id": thumb_id}


if __name__ == "__main__":
    # 测试
    test_html = """
    <p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); border-radius: 0;">
    <span style="font-size: 20px; color: #fff; font-weight: bold;">TrustMRR人物志</span>
    </p>
    <p style="margin: 20px; font-size: 15px;">测试内容...</p>
    """
    
    result = publish_article(
        title="深度解析Postiz：AI+开源如何实现207%增长",
        content=test_html,
        digest="深度5500字：Nevo David如何用AI+开源实现207%增长",
        source_url="https://postiz.com",
        subtitle="Nevo David创业故事"
    )
    print(result)
