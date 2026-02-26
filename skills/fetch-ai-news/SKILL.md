---
name: fetch-ai-news
description: 触发 AI News 抓取并发布到 Railway
triggers:
  - 命令: fetch news
  - 命令: 抓取新闻
  - 命令: AI News
---

# Fetch AI News Skill

当用户要求抓取 AI 新闻时，使用以下 curl 命令触发 Railway 上的 AI News 服务：

```bash
curl -s "https://ai-news-production-2735.up.railway.app/api/trigger"
```

## 使用方式

用户可以说：
- "fetch news"
- "抓取 AI 新闻"
- "更新 AI News"

## 返回

告诉用户新闻已成功抓取，并可以访问 https://ai-news-production-2735.up.railway.app 查看。
