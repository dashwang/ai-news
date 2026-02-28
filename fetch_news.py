#!/usr/bin/env python3
"""
AI News 自动抓取脚本
用于 Railway 部署
只抓取英文新闻，翻译和编辑由 OpenClaw 负责
"""

import os
import sys
import json
import sqlite3
import argparse
import feedparser
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "data/news.db")

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
    # Product Hunt
    "ProductHunt": {
        "url": "https://www.producthunt.com/feed",
        "top_n": 5,
        "icon": "https://www.producthunt.com/favicon.ico",
    },
    # SubStack Top AI Newsletters (ranked by popularity)
    "TheSequence": {
        "url": "https://thesequence.substack.com/feed",
        "top_n": 2,
        "icon": "https://thesequence.substack.com/favicon.ico",
    },
    "AheadofAI": {
        "url": "https://www.aheadofai.com/feed",
        "top_n": 2,
        "icon": "https://www.aheadofai.com/favicon.ico",
    },
    "LatentSpace": {
        "url": "https://www.latent.space/feed",
        "top_n": 2,
        "icon": "https://www.latent.space/favicon.ico",
    },
    "BenEvans": {
        "url": "https://www.benevans.com/feed",
        "top_n": 2,
        "icon": "https://www.benevans.com/favicon.ico",
    },
    "ExponentialView": {
        "url": "https://www.exponentialview.co/feed",
        "top_n": 2,
        "icon": "https://www.exponentialview.co/favicon.ico",
    },
    "LastWeekinAI": {
        "url": "https://lastweekinai.substack.com/feed",
        "top_n": 2,
        "icon": "https://lastweekinai.substack.com/favicon.ico",
    },
    "ImportAI": {
        "url": "https://jack-clark.net/import-ai/feed",
        "top_n": 2,
        "icon": "https://jack-clark.net/favicon.ico",
    },
    "Superhuman": {
        "url": "https://blog.superhuman.com/feed",
        "top_n": 2,
        "icon": "https://blog.superhuman.com/favicon.ico",
    },
    "OneUsefulThing": {
        "url": "https://oneusefulthing.substack.com/feed",
        "top_n": 2,
        "icon": "https://oneusefulthing.substack.com/favicon.ico",
    },
    "Interconnects": {
        "url": "https://interconnects.ai/feed",
        "top_n": 2,
        "icon": "https://interconnects.ai/favicon.ico",
    },
    "SemiAnalysis": {
        "url": "https://www.semianalysis.com/feed",
        "top_n": 2,
        "icon": "https://www.semianalysis.com/favicon.ico",
    },
}


def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
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


def fetch_rss_source(source_name: str, config: dict) -> list:
    items = []
    try:
        feed = feedparser.parse(config["url"])
        for entry in feed.entries[: config.get("top_n", 5)]:
            score = 0
            if hasattr(entry, "likes"):
                try:
                    score = int(entry.likes) if entry.likes else 0
                except:
                    pass

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
    all_news = []
    for source_name, config in SOURCES.items():
        items = fetch_rss_source(source_name, config)
        all_news.extend(items)
    return all_news


def save_news(news_items: list, date: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news WHERE date LIKE ?", (date + "%",))

    for item in news_items:
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
                "",
                "",
                item.get("icon", ""),
            ),
        )

    conn.commit()
    conn.close()
    print(f"Saved {len(news_items)} news items")


def get_news_json(date: str = None) -> dict:
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    conn = get_db()
    cursor = conn.cursor()
    
    # 按自然顺序获取所有数据
    cursor.execute(
        "SELECT source, title, url, summary, score, icon FROM news WHERE date LIKE ?",
        (date + "%",),
    )
    rows = cursor.fetchall()
    conn.close()

    # 按要求的格式组织
    news_data = {
        "HackerNews": [],
        "ProductHunt": [],
        "TechCrunch": [],
        "SubStack": []
    }
    
    # 先收集所有 SubStack 文章用于排序
    all_substack = []
    
    for row in rows:
        source = row["source"]
        item = {
            "source": row["source"],
            "title": row["title"],
            "url": row["url"],
            "summary": row["summary"],
            "score": row["score"],
            "icon": row["icon"],
        }
        
        if source == "HackerNews":
            news_data["HackerNews"].append(item)
        elif source == "ProductHunt":
            news_data["ProductHunt"].append(item)
        elif source == "TechCrunch":
            news_data["TechCrunch"].append(item)
        else:
            # 其他来源归入 SubStack
            all_substack.append(item)
    
    # SubStack 按热点分排序
    all_substack.sort(key=lambda x: x.get("score", 0), reverse=True)
    news_data["SubStack"] = all_substack

    return {"date": date, "news": news_data, "status": "ok"}


def main(date: str = None):
    print("=" * 50)
    print("AI News Fetcher Started")
    print(f"Time: {datetime.now()}")
    if date:
        print(f"Date: {date}")
    print("=" * 50)

    init_db()

    print("\nFetching news...")
    news = fetch_all_news()
    print(f"Fetched {len(news)} items")

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    print(f"\nSaving to database...")
    save_news(news, date)

    print("\nAI News Fetcher Completed!")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI News Fetcher")
    parser.add_argument("--date", type=str, help="Date in YYYY-MM-DD format")
    args = parser.parse_args()

    success = main(args.date)
    sys.exit(0 if success else 1)
