# AI News 自动发布脚本
# 用于 Railway 定时任务
# 设置环境变量: WECHAT_APP_ID, WECHAT_APP_SECRET

import os
import sys
import json
import requests
import datetime

# Railway API 地址
RAILWAY_API = "https://ai-news-production-2735.up.railway.app"

# 微信公众号凭证 (从环境变量获取)
WECHAT_APP_ID = os.environ.get("WECHAT_APP_ID", "")
WECHAT_APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "")


def get_wechat_token():
    """获取微信 access_token"""
    if not WECHAT_APP_ID or not WECHAT_APP_SECRET:
        print("⚠️ 未配置微信凭证")
        return None
    
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if "access_token" in data:
            return data["access_token"]
        else:
            print(f"获取token失败: {data}")
            return None
    except Exception as e:
        print(f"获取token异常: {e}")
        return None


def publish_to_wechat(token, title, content):
    """发布到微信公众号草稿箱"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    data = {
        "articles": [{
            "title": title,
            "author": "科技日报",
            "content": content,
            "digest": content[:120].replace("\n", " "),
            "source_url": "https://veray.ai"
        }]
    }
    try:
        resp = requests.post(url, json=data, timeout=30)
        return resp.json()
    except Exception as e:
        print(f"发布异常: {e}")
        return {"errcode": -1, "errmsg": str(e)}


def generate_content(news_data):
    """生成公众号文章内容"""
    
    hn_news = news_data.get("news", {}).get("HackerNews", [])[:5]
    lenny_news = news_data.get("news", {}).get("LennysNewsletter", [])[:3]
    lex_news = news_data.get("news", {}).get("LexFridman", [])[:2]
    tc_news = news_data.get("news", {}).get("TechCrunch", [])[:5]
    
    date = datetime.datetime.now().strftime("%Y.%m.%d")
    
    # 封面
    content = f"""<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); border-radius: 0;"><span style="font-size: 14px; color: #fff; opacity: 0.9;">📰 科技日报</span></p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">🔥 {date} 科技圈发生了什么？</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">这一周的科技圈，信息量有点大</p>"""
    
    # Hacker News
    content += """<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600;"><strong style="font-size: 16px; color: #ff6600;">🔥 Hacker News 热门</strong></p>"""
    for i, item in enumerate(hn_news, 1):
        title = item.get("title", "")[:60]
        summary = item.get("summary", "")[:140] if item.get("summary") else "点击查看详情"
        summary = summary.replace("<a href=", "<a href=").replace("</a>", "</a>")
        content += f"""<p style="margin: 15px 0 5px 0;"><strong style="font-size: 15px; color: #1a1a1a;">{i}. {title}</strong></p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">{summary}</p>
<p style="margin: 5px 0 15px 0; border-bottom: 1px dashed #eee;"></p>"""
    
    # SubStack
    substack_news = lenny_news + lex_news
    content += """<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff5e6; border-radius: 8px; border-left: 4px solid #ff4400;"><strong style="font-size: 16px; color: #ff4400;">💡 SubStack 精选</strong></p>"""
    for i, item in enumerate(substack_news, 1):
        title = item.get("title", "")[:60]
        summary = item.get("summary", "")[:140] if item.get("summary") else "点击查看详情"
        content += f"""<p style="margin: 15px 0 5px 0;"><strong style="font-size: 15px; color: #1a1a1a;">{i}. {title}</strong></p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">{summary}</p>
<p style="margin: 5px 0 15px 0; border-bottom: 1px dashed #eee;"></p>"""
    
    # TechCrunch
    content += """<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #e8f5e9; border-radius: 8px; border-left: 4px solid #0a9900;"><strong style="font-size: 16px; color: #0a9900;">📱 TechCrunch 科技</strong></p>"""
    for i, item in enumerate(tc_news, 1):
        title = item.get("title", "")[:60]
        summary = item.get("summary", "")[:140] if item.get("summary") else "点击查看详情"
        content += f"""<p style="margin: 15px 0 5px 0;"><strong style="font-size: 15px; color: #1a1a1a;">{i}. {title}</strong></p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">{summary}</p>
<p style="margin: 5px 0 15px 0; border-bottom: 1px dashed #eee;"></p>"""
    
    # 结尾
    content += """<p style="text-align: center; margin-top: 30px; padding: 25px 20px; background: #fafafa; border-radius: 12px; border: 1px solid #eee;"><span style="font-size: 16px; color: #333; font-weight: 500;">👍 觉得有用？不妨分享给朋友 👏</span></p>
<p style="text-align: center; margin-top: 20px; font-size: 13px; color: #999; line-height: 1.6;">📱 <strong>每天早上8点</strong>整理送达 | 点个关注不迷路<br>💬 欢迎评论交流，说说你的看法</p>
<p style="text-align: center; margin-top: 15px; font-size: 11px; color: #ccc; letter-spacing: 1px;">© 2026 科技日报 | 认真做内容</p>"""
    
    title = f"🔥 {date} 科技日报 | 20条热点"
    return title, content


def main():
    print("=" * 50)
    print("AI News 自动发布系统")
    print(f"Time: {datetime.datetime.now()}")
    print("=" * 50)
    
    # 1. 抓取新闻
    print("\n[1/3] 抓取新闻...")
    try:
        resp = requests.get(f"{RAILWAY_API}/api/fetch", timeout=30)
        news_data = resp.json()
        print(f"  ✅ 抓取成功")
    except Exception as e:
        print(f"  ❌ 抓取失败: {e}")
        return False
    
    # 2. 生成内容
    print("\n[2/3] 生成文章...")
    title, content = generate_content(news_data)
    print(f"  ✅ 标题: {title[:30]}...")
    
    # 3. 发布到微信
    print("\n[3/3] 发布到微信...")
    token = get_wechat_token()
    if not token:
        print("  ⚠️ 跳过发布 (未配置微信)")
        return True
    
    result = publish_to_wechat(token, title, content)
    if result.get("errcode") == 0:
        print(f"  ✅ 发布成功!")
        print(f"  media_id: {result.get('media_id')}")
    else:
        print(f"  ❌ 发布失败: {result}")
        return False
    
    print("\n✅ 全部完成!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
