---
name: fetch-news
description: 从RSS源抓取AI新闻，保存到news_raw.json
triggers:
  - 命令: fetch news
  - 命令: 抓取AI新闻
  - 命令: 拉取AI新闻

# 输出文件
OUTPUT_FILE: "news_raw.json"

# 去重配置
DUPLICATE_FILE: "published_articles.json"

# 新闻源
SOURCES:
  HackerNews:
    url: "https://news.ycombinator.com/rss"
    top_n: 10
  TechCrunch:
    url: "https://techcrunch.com/feed/"
    top_n: 5
  ProductHunt:
    url: "https://www.producthunt.com/feed"
    top_n: 5
  TheSequence:
    url: "https://thesequence.substack.com/feed"
    top_n: 3
  LatentSpace:
    url: "https://www.latent.space/feed"
    top_n: 2

---

# Fetch News Worker

## 功能
1. 从RSS源抓取AI新闻
2. 过滤重复内容（比对published_articles.json）
3. 保存到news_raw.json

## 执行命令

```bash
cd ~/Projects/llms/agent/ai-news

python3 fetch_worker.py
# 或指定输出文件
python3 fetch_worker.py -o my_news.json
```

## 输出
news_raw.json格式:
```json
[
  {
    "id": "uuid",
    "source": "HackerNews",
    "title": "...",
    "url": "...",
    "summary": "...",
    "timestamp": "ISO8601"
  }
]
```

## 检查清单
- [ ] 抓取到新闻条目
- [ ] 过滤重复内容
- [ ] 保存到news_raw.json
- [ ] 打印抓取统计