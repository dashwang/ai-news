#!/usr/bin/env python3
"""
生成文章封面图片
根据标题动态生成匹配的封面
"""

import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import sys

# 预选配图（根据主题）
IMAGE_URLS = {
    "postiz": "https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=900",
    "social": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=900",
    "ai": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900",
    "default": "https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?w=900",
}


def get_matching_image_url(title, keywords=None):
    """根据标题关键词匹配图片"""
    title_lower = title.lower()
    
    # 关键词匹配
    if any(k in title_lower for k in ["postiz", "社交媒体", "social media"]):
        return IMAGE_URLS["postiz"]
    elif any(k in title_lower for k in ["ai", "人工智能", "gpt", "openai"]):
        return IMAGE_URLS["ai"]
    elif any(k in title_lower for k in ["增长", "growth", "创业", "startup"]):
        return IMAGE_URLS["social"]
    
    return IMAGE_URLS["default"]


def download_image(url):
    """下载图片"""
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        return Image.open(BytesIO(resp.content))
    return None


def generate_cover(title, subtitle="", image_url=None):
    """生成封面图片"""
    # 获取匹配的配图
    if not image_url:
        image_url = get_matching_image_url(title)
    
    print(f"📷 使用配图: {image_url}")
    
    # 下载背景图
    bg_img = download_image(image_url)
    if bg_img:
        # 调整大小为 900x383
        bg_img = bg_img.resize((900, 383), Image.LANCZOS)
    else:
        # 如果下载失败，使用蓝色背景
        bg_img = Image.new("RGB", (900, 383), color="#1a1a3e")
    
    # 创建可绘制对象
    draw = ImageDraw.Draw(bg_img)
    
    # 添加半透明黑色遮罩（让文字更清晰）
    overlay = Image.new("RGBA", (900, 383), (0, 0, 0, 100))
    bg_img = Image.alpha_composite(bg_img.convert("RGBA"), overlay)
    bg_img = bg_img.convert("RGB")
    draw = ImageDraw.Draw(bg_img)
    
    # 加载字体
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 处理标题（处理长标题）
    display_title = title[:28] + "..." if len(title) > 28 else title
    
    # 绘制标题（白色）
    draw.text((450, 140), display_title, font=font_title, fill="#ffffff", anchor="mm")
    
    # 绘制副标题（橙色）
    if subtitle:
        draw.text((450, 200), subtitle, font=font_subtitle, fill="#ff6600", anchor="mm")
    
    # 绘制底部信息（青色）
    draw.text((450, 320), "TrustMRR人物志", font=font_small, fill="#4ecdc4", anchor="mm")
    draw.text((450, 350), "扫码关注 · grepAI", font=font_small, fill="#aaaaaa", anchor="mm")
    
    return bg_img


if __name__ == "__main__":
    # 测试生成
    title = "深度解析Postiz：AI+开源如何实现207%增长"
    subtitle = "Nevo David创业故事"
    
    img = generate_cover(title, subtitle)
    
    # 保存并显示
    img.save("/root/.openclaw/workspace/cover_postiz.jpg", "JPEG", quality=95)
    print("✅ 封面已保存: /root/.openclaw/workspace/cover_postiz.jpg")
