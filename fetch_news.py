#!/usr/bin/env python3
"""
AI News 自动抓取和发布脚本
用于 Railway 部署
"""

import os
import sys
import json
import sqlite3
import time
import feedparser
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# 配置
TRANSLATION_API_URL = os.environ.get(
    "TRANSLATION_API_URL", "http://127.0.0.1:5003/translate"
)
DATABASE_URL = os.environ.get("DATABASE_URL", "data/news.db")

# 新闻源配置
SOURCES = {
    "TechCrunch": {
        "url": "https://techcrunch.com/feed/",
        "top_n": 5,
        "icon": "https://techcrunch.com/favicon.ico",
    },
    "HackerNews": {
        "url": "https://news.ycombinator.com/rss",
        "top_n": 5,
        "icon": "https://news.ycombinator.com/favicon.ico",
    },
    "OpenAI": {
        "url": "https://openai.com/blog/rss.xml",
        "top_n": 5,
        "icon": "https://openai.com/favicon.ico",
    },
}


def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库"""
    os.makedirs(os.path.dirname(DATABASE_URL) or ".", exist_ok=True)
    conn = sqlite3.connect(DATABASE_URL)
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


def translate_text(text: str) -> str:
    """翻译文本到中文"""
    if not text:
        return ""
    try:
        resp = requests.post(TRANSLATION_API_URL, json={"text": text}, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("translated_text", text)
    except Exception as e:
        print(f"Translation error: {e}")
    return text


def fetch_rss_source(source_name: str, config: dict) -> list:
    """从 RSS 源抓取新闻"""
    items = []
    try:
        feed = feedparser.parse(config["url"])
        for entry in feed.entries[: config.get("top_n", 5)]:
            score = 0
            if hasattr(entry, "likes"):
                score = int(entry.likes) if entry.likes else 0

            url = entry.link if hasattr(entry, "link") else ""
            title = entry.title if hasattr(entry, "title") else ""
            summary = ""
            if hasattr(entry, "summary"):
                summary = entry.summary[:500]
            elif hasattr(entry, "description"):
                summary = entry.description[:500]

            items.append(
                {
                    "source": source_name,
                    "title": title,
                    "url": url,
                    "content": "",
                    "summary": summary,
                    "score": score,
                    "icon": config.get("icon", ""),
                }
            )
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")
    return items


def fetch_hackernews() -> list:
    """抓取 Hacker News"""
    items = []
    try:
        feed = feedparser.parse("https://news.ycombinator.com/rss")
        for entry in feed.entries[:5]:
            title = entry.title
            url = entry.link

            score = 0
            if hasattr(entry, "tags"):
                for tag in entry.tags:
                    if hasattr(tag, "term"):
                        try:
                            score = int(tag.term.split(" ")[0])
                        except:
                            pass

            items.append(
                {
                    "source": "HackerNews",
                    "title": title,
                    "url": url,
                    "content": "",
                    "summary": "",
                    "score": score,
                    "icon": "https://news.ycombinator.com/favicon.ico",
                }
            )
    except Exception as e:
        print(f"Error fetching HackerNews: {e}")
    return items


def fetch_all_news() -> list:
    """抓取所有源的新闻"""
    all_news = []

    # 抓取 RSS 源
    for source_name, config in SOURCES.items():
        items = fetch_rss_source(source_name, config)
        all_news.extend(items)

    # 抓取 HackerNews
    all_news.extend(fetch_hackernews())

    return all_news


def save_news(news_items: list, date: str):
    """保存新闻到数据库"""
    conn = get_db()
    cursor = conn.cursor()

    # 删除当天该来源的新闻
    cursor.execute("DELETE FROM news WHERE date LIKE ?", (date + "%",))

    for item in news_items:
        title_zh = translate_text(item["title"])
        summary_zh = translate_text(item.get("summary", "")[:300])

        cursor.execute(
            """
            INSERT INTO news (source, title, url, content, summary, score, date, title_zh, summary_zh, icon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                item["source"],
                item["title"],
                item["url"],
                item.get("content", ""),
                item.get("summary", ""),
                item.get("score", 0),
                date,
                title_zh,
                summary_zh,
                item.get("icon", ""),
            ),
        )

    conn.commit()
    conn.close()
    print(f"✅ Saved {len(news_items)} news items")


def main():
    print("=" * 50)
    print("🤖 AI News Bot Started")
    print(f"Time: {datetime.now()}")
    print("=" * 50)

    # 初始化数据库
    init_db()

    # 抓取新闻
    print("\n📥 Fetching news...")
    news = fetch_all_news()
    print(f"Fetched {len(news)} items")

    # 保存新闻
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n💾 Saving to database...")
    save_news(news, today)

    print("\n✅ AI News Bot Completed!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
