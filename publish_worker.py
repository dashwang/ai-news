#!/usr/bin/env python3
"""
Publish WeChat Worker - 读取翻译后的新闻，发布到公众号草稿箱
"""

import os
import sys
import json
import random
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import tempfile

INPUT_FILE = "news_translated.json"
DUPLICATE_FILE = "published_articles.json"

WECHAT_APP_ID = os.environ.get("WECHAT_APP_ID", "wxa87b65ba78d3c822")
WECHAT_APP_SECRET = os.environ.get(
    "WECHAT_APP_SECRET", "ac6a029c2b4ef7c1b89fbaeeaace3931"
)


def load_published():
    try:
        with open(DUPLICATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("articles", [])
    except:
        return []


def save_published(article: dict):
    articles = load_published()
    articles.append(
        {
            "title": article.get("title", ""),
            "title_zh": article.get("title_zh", ""),
            "source": article.get("source", ""),
            "published_at": datetime.now().isoformat(),
        }
    )
    with open(DUPLICATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"articles": articles, "titles": [a["title"] for a in articles]},
            f,
            ensure_ascii=False,
        )


def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}"
    resp = requests.get(url, timeout=10)
    data = resp.json()
    if "access_token" in data:
        return data["access_token"]
    raise Exception(f"获取token失败: {data}")


def upload_cover_image(token):
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


def generate_html(news_items: list) -> str:
    import subprocess
    import json as json_lib

    date_str = datetime.now().strftime("%Y.%m.%d")
    hour = datetime.now().hour

    if hour < 12:
        time_label = "早报"
    elif hour < 18:
        time_label = "午报"
    else:
        time_label = "晚报"

    prompt = f"""你是一位专业的 AI 科技公众号编辑。请分析以下新闻条目，筛选并整理成公众号文章。

要求：
1. 选出 6-8 条最具价值的新闻，按重要程度排序
2. 每条新闻需要：标题(简练，20字内)、摘要(50-80字)、一句话点评
3. 分类整理：重点要闻、行业动态、技术前沿
4. 标题要吸引眼球但不夸张
5. 点评要有观点，不是空话

新闻条目：
{json_lib.dumps(news_items, ensure_ascii=False, indent=2)}

请返回以下 JSON 格式：
{{
    "opening": "一句科技感开场白",
    "categories": [
        {{"title": "分类名", "items": [
            {{"title": "标题", "summary": "摘要", "comment": "点评"}}
        ]}}
    ]
}}
"""

    try:
        result = subprocess.run(
            ["claude", "--print", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=180,
        )
        llm_output = result.stdout.strip()

        if llm_output.startswith("```"):
            llm_output = llm_output.split("```")[1]
            if llm_output.startswith("json"):
                llm_output = llm_output[4:].strip()

        structured = json_lib.loads(llm_output)
    except Exception as e:
        print(f"⚠️ LLM 调用失败: {e}, 使用默认模板")
        structured = None

    if not structured:
        openings = [
            "Claude Code 源码意外泄露，1-bit 大模型商业化，本期 AI 午报聚焦今日最值得关注的动态。",
            "大模型领域今日持续热闹。模型压缩、 AI 安全、企业应用多点开花，机器之心整理今日要闻。",
        ]
        structured = {
            "opening": random.choice(openings),
            "categories": [
                {
                    "title": "🔥 重点要闻",
                    "items": [
                        {
                            "title": "Claude Code 源码泄露事件",
                            "summary": "Claude Code 意外开源，为开发者提供深入理解其架构的机会。",
                            "comment": "AI 安全与开源的边界值得思考。",
                        },
                        {
                            "title": "1-Bit Bonsai 商业化",
                            "summary": "首个商业化 1-bit 大语言模型发布，大幅降低推理成本。",
                            "comment": "模型量化进入新阶段。",
                        },
                    ],
                },
                {
                    "title": "💼 行业动态",
                    "items": [
                        {
                            "title": "Mercor 遭网络攻击",
                            "summary": "AI 招聘初创公司确认安全事件，与 LiteLLM 漏洞有关。",
                            "comment": "开源依赖安全审计刻不容缓。",
                        },
                        {
                            "title": "Robotaxi 拒绝透露数据",
                            "summary": "主要自动驾驶企业拒绝公开远程协助频率。",
                            "comment": "透明度仍是行业痛点。",
                        },
                    ],
                },
                {
                    "title": "🔬 技术前沿",
                    "items": [
                        {
                            "title": "TinyLoRA 实现突破",
                            "summary": "仅用 13 个参数即可实现推理能力。",
                            "comment": "极简模型也值得探索。",
                        },
                    ],
                },
            ],
        }

    html = f"""
<div style="padding: 20px; max-width: 800px; margin: 0 auto; background: #fff;">
<p style="text-align: center; font-size: 24px; font-weight: bold; padding: 18px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #fff; border-radius: 8px; margin-bottom: 20px;">{date_str} AI {time_label} · grepAI</p>
<p style="color: #666; font-size: 15px; line-height: 1.8; margin-bottom: 25px; padding: 0 10px;">{structured.get("opening", "")}</p>
"""

    for cat in structured.get("categories", []):
        html += f'<h3 style="color: #1a1a2e; font-size: 17px; font-weight: bold; border-left: 4px solid #e94560; padding-left: 12px; margin: 25px 0 15px;">{cat.get("title", "")}</h3>'

        for item in cat.get("items", []):
            html += f"""<div style="margin: 18px 0; padding: 15px; background: #f8f9fa; border-radius: 8px;">
<p style="margin: 0 0 8px;"><strong style="color: #1a1a2e; font-size: 16px;">{item.get("title", "")}</strong></p>
<p style="margin: 0 0 10px; color: #555; font-size: 14px; line-height: 1.7;">{item.get("summary", "")}</p>
<p style="margin: 0; color: #e94560; font-size: 13px; font-style: italic;">💡 {item.get("comment", "")}</p>
</div>"""

    html += f"""
<div style="text-align: center; margin-top: 30px; padding: 25px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px;">
<img src="https://mmbiz.qpic.cn/sz_mmbiz_jpg/Rv7jxicObXS3EVWAxcKy4hkx7aJof9P3lnR95L6UkOPNRbKFHxC8EDvGb7XeUibKnY8XpxaCrTm7MLibW5BDKzt56EgicicM8NK1qC62uGVb1lXg/640?wx_fmt=jpeg&from=appmsg" style="max-width: 35%; width: 130px; height: auto; border-radius: 10px;">
<p style="margin: 20px 0 0; color: #888; font-size: 14px;">关注「grepAI」</p>
<p style="margin: 5px 0 0; color: #aaa; font-size: 12px;">获取每日 AI 前沿动态</p>
<p style="margin: 20px 0 0; color: #999; font-size: 13px;">你觉得本期哪条新闻最值得关注？</p>
</div>
</div>"""
    return html


def main():
    print("=" * 50)
    print("📝 Publish WeChat Worker Started")
    print(f"Time: {datetime.now()}")
    print("=" * 50)

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file not found: {INPUT_FILE}")
        return False

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        news_items = json.load(f)

    print(f"\n📥 Loaded {len(news_items)} items from {INPUT_FILE}")

    published_titles = {a["title"] for a in load_published()}
    filtered_items = [n for n in news_items if n.get("title") not in published_titles]
    print(f"✅ After deduplication: {len(filtered_items)} items")

    if not filtered_items:
        print("❌ No news to publish")
        return False

    print(f"\n📝 Generating article with {len(filtered_items)} items...")
    content = generate_html(filtered_items)

    date_str = datetime.now().strftime("%Y.%m.%d")
    hour = datetime.now().hour
    time_label = ["早报", "午报", "晚报"][hour // 6]
    title = f"{date_str} 全球AI科技{time_label}"

    try:
        print("\n🔑 Getting access token...")
        token = get_access_token()

        print("📤 Uploading cover...")
        thumb_id = upload_cover_image(token)

        print("📝 Creating draft...")
        article = {
            "title": title,
            "author": "grepAI",
            "content": content,
            "digest": title,
            "thumb_media_id": thumb_id,
            "content_source_url": "https://veray.ai",
        }

        media_id = create_draft(token, [article])

        for item in filtered_items:
            save_published(item)

        print(f"\n✅ Draft created: {media_id}")
        print(f"✅ Published {len(filtered_items)} items")
    except Exception as e:
        print(f"\n⚠️ WeChat publish failed: {e}")
        print("📄 Generating HTML preview instead...")

        preview_file = "article_preview.html"
        with open(preview_file, "w", encoding="utf-8") as f:
            full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .article {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div class="article">
        {content}
    </div>
</body>
</html>"""
            f.write(full_html)

        print(f"✅ HTML preview saved to: {preview_file}")

        for item in filtered_items:
            save_published(item)

        print(f"✅ Saved {len(filtered_items)} items to published_articles.json")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
