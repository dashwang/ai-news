#!/usr/bin/env python3
"""
Fetch News Worker - 从RSS源抓取AI新闻，保存到文件供下一个worker使用
"""

import os
import sys
import json
import uuid
import sqlite3
import argparse
import feedparser
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "data/news.db")
OUTPUT_FILE = os.environ.get("OUTPUT_FILE", "news_raw.json")

SOURCES = {
    "HackerNews": {"url": "https://news.ycombinator.com/rss", "top_n": 10},
    "TechCrunch": {"url": "https://techcrunch.com/feed/", "top_n": 5},
    "ProductHunt": {"url": "https://www.producthunt.com/feed", "top_n": 5},
    "TheSequence": {"url": "https://thesequence.substack.com/feed", "top_n": 3},
    "LatentSpace": {"url": "https://www.latent.space/feed", "top_n": 2},
}


def load_published():
    try:
        with open("published_articles.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("titles", []))
    except:
        return set()


def fetch_rss_source(source_name: str, config: dict) -> list:
    items = []
    try:
        feed = feedparser.parse(config["url"])
        for entry in feed.entries[: config.get("top_n", 5)]:
            url = entry.link if hasattr(entry, "link") else ""
            title = entry.title if hasattr(entry, "title") else ""
            summary = ""
            if hasattr(entry, "summary"):
                summary = entry.summary[:500]
            elif hasattr(entry, "description"):
                summary = entry.description[:500]

            items.append(
                {
                    "id": str(uuid.uuid4()),
                    "source": source_name,
                    "title": title,
                    "url": url,
                    "summary": summary,
                    "timestamp": datetime.now().isoformat(),
                }
            )
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")
    return items


def main(output_file=None):
    print("=" * 50)
    print("🤖 Fetch News Worker Started")
    print(f"Time: {datetime.now()}")
    print("=" * 50)

    output_file = output_file or OUTPUT_FILE

    print("\n📥 Fetching news from RSS feeds...")
    all_news = []
    for source_name, config in SOURCES.items():
        items = fetch_rss_source(source_name, config)
        all_news.extend(items)
    print(f"✅ Fetched {len(all_news)} items")

    published_titles = load_published()
    filtered_news = [n for n in all_news if n["title"] not in published_titles]
    print(f"✅ After deduplication: {len(filtered_news)} items")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_news, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved to {output_file}")

    print("\n✨ Fetch News Worker Completed!")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch News Worker")
    parser.add_argument("--output", "-o", default="news_raw.json", help="Output file")
    args = parser.parse_args()

    success = main(args.output)
    sys.exit(0 if success else 1)
