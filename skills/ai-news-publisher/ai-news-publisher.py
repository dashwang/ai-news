#!/usr/bin/env python3
"""
AI News 自动发布系统
每天早上8点：抓取 → 翻译 → 编排 → 发布公众号
"""

import os
import json
import requests
import datetime
from openai import OpenAI

# ========== 配置区 ==========
# Vercel AI News API
VERCEL_API = "https://ai-news-teal-eight.vercel.app/"

# 微信公众号凭证 (需要从微信开放平台获取)
WECHAT_APP_ID = os.getenv("WECHAT_APP_ID", "你的AppID")
WECHAT_APP_SECRET = os.getenv("WECHAT_APP_SECRET", "你的AppSecret")

# OpenAI API (翻译用)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "你的OpenAI API Key")
MODEL = "gpt-4o-mini"

# ========== 微信公众号 API ==========
def get_wechat_access_token():
    """获取微信 access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}"
    resp = requests.get(url).json()
    return resp.get("access_token")

def publish_wechat_article(access_token, title, content, author="AI News"):
    """发布到微信公众号"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    # 生成永久图文链接
    content_html = f"""
<p><strong>📰 {title}</strong></p>
<p></p>
<p>作者：{author}</p>
<p>发布日期：{datetime.datetime.now().strftime('%Y-%m-%d')}</p>
<p></p>
<hr />
{content}
<p></p>
<hr />
<p>📱 关注更多AI资讯</p>
"""
    
    data = {
        "articles": [{
            "title": title,
            "author": author,
            "content": content_html,
            "content_source_url": "",
            "digest": content[:120] + "...",
            "show_cover_pic": 1,
        }]
    }
    
    resp = requests.post(url, json=data).json()
    return resp

# ========== 新闻抓取 ==========
def fetch_ai_news():
    """从 Vercel 抓取 AI 新闻"""
    resp = requests.get(VERCEL_API)
    return resp.text

# ========== 翻译 + 编排 ==========
def translate_and_edit(news_content):
    """用 LLM 翻译并编辑成专业文章"""
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = f"""你是一位资深的科技编辑。请将下面的 AI 新闻翻译成中文，并进行专业化编排：

要求：
1. 翻译准确、通顺
2. 标题吸引眼球
3. 内容按重要性排序
4. 添加适当的emoji
5. 结尾加一句引导评论的话

新闻内容：
{news_content}
"""
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# ========== 主流程 ==========
def main():
    print(f"🤖 [{datetime.datetime.now()}] 开始执行 AI News 自动发布...")
    
    # 1. 抓取新闻
    print("📥 抓取 AI 新闻...")
    news = fetch_ai_news()
    
    # 2. 翻译 + 编排
    print("✍️  翻译并编排文章...")
    article = translate_and_edit(news)
    
    # 提取标题（简单处理）
    title = "AI日报 | " + datetime.datetime.now().strftime('%Y-%m-%d')
    
    # 3. 发布公众号
    print("📤 发布到微信公众号...")
    token = get_wechat_access_token()
    result = publish_wechat_article(token, title, article)
    
    if result.get("errcode") == 0:
        print("✅ 发布成功！")
    else:
        print(f"❌ 发布失败: {result}")
    
    return result

if __name__ == "__main__":
    main()
