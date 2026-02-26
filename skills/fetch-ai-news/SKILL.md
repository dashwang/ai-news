---
name: fetch-ai-news
description: 抓取北美AI新闻，翻译成中文，编排后发布到微信公众号草稿箱
triggers:
  - 命令: fetch news
  - 命令: 抓取AI新闻
  - 命令: 发布AI新闻
  - 命令: AI News
---

# AI News 完整流程

当用户要求抓取并发布AI新闻时，执行以下完整流程：

## API 基础信息

- **Railway URL**: `https://ai-news-production-2735.up.railway.app`

## Step 1: 调用 Railway 获取英文新闻

使用 curl 调用 `/api/fetch` 接口：

```bash
curl "https://ai-news-production-2735.up.railway.app/api/fetch"
```

返回格式：
```json
{
  "status": "ok",
  "date": "2026-02-26",
  "news": {
    "TechCrunch": [
      {
        "source": "TechCrunch",
        "title": "OpenAI Announces GPT-5",
        "url": "https://techcrunch.com/...",
        "summary": "...",
        "score": 150,
        "icon": "..."
      }
    ],
    "HackerNews": [...],
    "OpenAI": [...]
  }
}
```

## Step 2: 翻译并编辑 (使用内嵌的 Minimax 模型)

对于每条新闻：

1. **翻译**: 将英文标题和摘要翻译成中文
2. **编辑**: 像资深编辑一样重新组织内容
   - 添加吸引眼球的引导语
   - 保持内容简洁有力
   - 按来源分组，每组3-5条精选
   - 添加emoji表情

3. **生成最终文章内容** (HTML格式，微信公众号兼容):

```html
<p style="text-align: center; font-size: 20px; font-weight: bold;">📅 2026.02.26 全球AI科技早报</p>
<p style="text-align: center; color: #888; font-size: 12px;">🔥 今日热榜</p>

<p>Hello 各位科技人～ 今日AI圈都有哪些大事件？速览👇</p>

<p style="font-size: 18px; font-weight: bold;">🔥 Hacker News 热门</p>
<p><strong>1. 🎉 标题（中文）</strong></p>
<p style="color:#666; font-size:13px;">摘要内容...</p>
<p style="color:#1976d2; font-size:11px;">🔗 原文链接</p>

<p style="font-size: 18px; font-weight: bold;">🧠 OpenAI 最新</p>
...

<p style="background:#f5f5f5; padding:12px; border-radius:8px;">📌 关注我们，每日获取 AI 科技前沿资讯！</p>
```

## Step 3: 发布到微信公众号草稿箱

构造 articles 数组并调用 Railway API：

```bash
curl -X POST "https://ai-news-production-2735.up.railway.app/api/publish_wechat" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [
      {
        "title": "2026.02.26 全球AI科技早报",
        "content": "<p>...生成的HTML内容...</p>",
        "digest": "今日精选全球AI科技资讯",
        "source_url": "https://veray.ai"
      }
    ]
  }'
```

## 返回结果

告诉用户：
1. 成功抓取了 X 条新闻
2. 已翻译并编辑完成
3. 已发布到微信公众号草稿箱
4. 提醒用户去公众号后台确认并发布
