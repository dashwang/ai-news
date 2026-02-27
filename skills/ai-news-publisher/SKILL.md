# AI News Publisher - 自动抓取翻译发布

## 概述

自动抓取 AI 新闻，翻译整理成公众号文章并发布。

## 数据源（4大平台）

1. **Hacker News** - `https://news.ycombinator.com/rss`
2. **SubStack (Lex Fridman + Lenny's Newsletter)** - `https://lexfridman.com/feed/` + `https://www.lennysnewsletter.com/feed`
3. **TechCrunch** - `https://techcrunch.com/feed/`
4. **Product Hunt** - `https://www.producthunt.com/feed`

## 抓取 API

```bash
curl "https://ai-news-production-2735.up.railway.app/api/fetch"
```

## 发布 API

```bash
curl -X POST "https://ai-news-production-2735.up.railway.app/api/publish_wechat" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [{
      "title": "标题",
      "content": "HTML内容",
      "digest": "摘要",
      "source_url": "https://veray.ai"
    }]
  }'
```

## 内容格式要求

### 结构要求

- **4大部分**：Hacker News、SubStack、TechCrunch、Product Hunt
- **每部分5条新闻**
- **每条140字左右**：标题 + 详细解读

### 标题格式示例

> **内存短缺导致智能手机出货量创十年最大降幅**  
> 据 IDC 预测，2026 年全球智能手机出货量将仅为 11.2 亿部，较去年的 12.6 亿部大幅下滑——这是十多年来最大的降幅。

### 文章结构

```html
<p style="text-align: center; font-size: 22px; font-weight: bold;">🔥 2026.02.27 AI 日报</p>
<p style="text-align: center; color: #888; font-size: 13px;">4大平台 · 20条热点</p>

<p><strong>🔥 Hacker News 热门</strong></p>
<p><strong>1. 新闻标题</strong></p>
<p>新闻内容...</p>

<p><strong>💡 SubStack 精选</strong></p>
...

<p><strong>📱 TechCrunch 科技</strong></p>
...

<p><strong>🚀 Product Hunt 热榜</strong></p>
...

<p style="text-align: center; margin-top: 20px;">📱 关注我们，获取每日科技前沿！</p>
```

## 常见问题

1. **Railway 500 错误** - 检查 RSS 源是否有效
2. **微信 IP 白名单** - 需要在微信开放平台添加 Railway 服务器 IP
3. **新闻不足20条** - 需要检查各 RSS 源是否正常返回数据

## 后续迭代方向

- [ ] 增加更多新闻源
- [ ] 自动翻译（接入翻译API）
- [ ] 个性化推荐（根据用户兴趣）
- [ ] 多平台发布（公众号、微博、Twitter）
- [ ] 评论互动分析
- [ ] 趋势预测
