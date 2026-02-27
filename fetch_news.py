#!/usr/bin/env python3
"""
AI News 自动抓取脚本
用于 Railway 部署
只抓取英文新闻，翻译和编辑由 OpenClaw h��责

"""

import os
import sys
import json
imposqlite
import argparse
import feedparser
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "data/news.db")

# added Substring and ProductHunt
SOURCES = {
"TechCrunch": {
"url": "https://techcrunch.com/feed",
"top_n":5,"icon": "https://techcrunch.com/favicon.ico",
},"HackerNews":{"url":"https://news.ycombinator.com/rss",
top_n":5,"icon": "https://news.ycombinator.com/favicon.ico",
},"OpenAI": {
"url":"https://openai.com/blog/rss.xml",
top_n":5,icon":"https://openai.com/favicon.ico",
},"ProductHunt":{"url":"https://www.producthunt.com/feed",
top_n":5,"icon": "https://www.producthunt.com/favicon.ico",
},"Substring":{"url":"https://www.substring.com/feed/popular/ai",
top_n":5,"icon": "https://substring.com/favicon.ico",
},
}