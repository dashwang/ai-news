# AI News Publisher - 自动抓取翻译发布

## 概述

自动抓取 AI 新闻，翻译整理成公众号文章并发布。

## 数据源（4大平台）

1. **Hacker News** - `https://news.ycombinator.com/rss`
2. **SubStack (Lex Fridman + Lenny's Newsletter)** - `https://lexfridman.com/feed/` + `https://www.lennysnewsletter.com/feed`
3. **TechCrunch** - `https://techcrunch.com/feed/`
4. **Product Hunt** - `https://www.producthunt.com/feed`

## Logo 资源

 logos保存在: `skills/ai-news-publisher/logos/`

- `logo-hackernews.png` - Hacker News _logo
- `logo-techcrunch.png` - TechCrunch logo
- `logo-producthunt.png` - Product Hunt logo
- `logo-lexfridman.png` - Lex Fridman logo
- `logo-lenny.png` - Lenny's Newsletter logo

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

## 微信公众号排版标准

### 整体风格

- 标题醒目，正文舒适
- 段落间距合理，重点突出
- 使用 emoji 增加活力
- 每条新闻140字左右

### 标题区样式

```html
<!-- 封面图 + 标题 -->
<p style="text-align: center; margin: 0; padding: 0;">
  <img src="https://your-cdn.com/cover-ai-news.jpg" style="width: 100%; max-width: 600px; border-radius: 8px;">
</p>
<p style="text-align: center; font-size: 24px; font-weight: bold; color: #1a1a1a; margin-top: 15px;">🔥 2026.02.27 AI 日报</p>
<p style="text-align: center; color: #888; font-size: 14px; margin-top: 5px;">4大平台 · 20条热点</p>
```

### 平台分区样式（带Logo）

```html
<!-- 分区标题 + Logo -->
<p style="margin: 25px 0 15px 0; padding: 10px 15px; background: #f5f5f5; border-radius: 8px;">
  <img src="https://your-cdn.com/logo-hackernews.png" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 8px;">
  <strong style="font-size: 16px; color: #ff6600;">🔥 Hacker News 热门</strong>
</p>
```

### 4大平台颜色主题

| 平台 | 颜色 | emoji |
|------|------|-------|
| Hacker News | #ff6600 | 🔥 |
| SubStack | #ff4400 | 💡 |
| TechCrunch | #0a9900 | 📱 |
| Product Hunt | #da552f | 🚀 |

### 单条新闻样式

```html
<p style="margin: 15px 0 5px 0;">
  <strong style="font-size: 15px; color: #1a1a1a;">1. 新闻标题</strong>
</p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">
  新闻内容...（140字左右）
</p>
<p style="margin: 5px 0 15px 0; border-bottom: 1px dashed #eee;"></p>
```

### 底部引导

```html
<p style="text-align: center; margin-top: 30px; padding: 20px; background: #f9f9f9; border-radius: 10px;">
  <span style="font-size: 16px;">📱 关注我们，获取每日科技前沿！</span>
</p>
```

## 完整示例

```html
<p style="text-align: center; margin: 0; padding: 0;">
  <img src="https://your-cdn.com/cover-ai-news.jpg" style="width: 100%; max-width: 600px; border-radius: 8px;">
</p>
<p style="text-align: center; font-size: 24px; font-weight: bold; color: #1a1a1a; margin-top: 15px;">🔥 2026.02.27 AI 日报</p>
<p style="text-align: center; color: #888; font-size: 14px; margin-top: 5px; margin-bottom: 25px;">4大平台 · 20条热点</p>

<!-- Hacker News -->
<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600;">
  <strong style="font-size: 16px; color: #ff6600;">🔥 Hacker News 热门</strong>
</p>

<p style="margin: 15px 0 5px 0;">
  <strong style="font-size: 15px; color: #1a1a1a;">1. Anthropic CEO 硬刚五角大楼：拒绝向军方开放 AI</strong>
</p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">
  Dario Amodei 明确表示问心无愧地拒绝五角大楼要求，向军方无条件开放 AI 系统的要求，与 OpenAI 此前的类似争议形成呼应，引发关于 AI 伦理与国家安全边界的热议。
</p>
<p style="margin: 5px 0 15px 0; border-bottom: 1px dashed #eee;"></p>

<!-- 其他平台... -->

<p style="text-align: center; margin-top: 30px; padding: 20px; background: #f9f9f9; border-radius: 10px;">
  <span style="font-size: 16px;">📱 关注我们，获取每日科技前沿！</span>
</p>
```

## 常见问题

1. **Railway 500 错误** - 检查 RSS 源是否有效
2. **微信 IP 白名单** - 需要在微信开放平台添加 Railway 服务器 IP
3. **新闻不足20条** - 需要检查各 RSS 源是否正常返回数据
4. **Logo 加载失败** - 建议将 Logo 上传到 CDN，使用永久链接

## 后续迭代方向

- [ ] 增加更多新闻源
- [ ] 自动翻译（接入翻译API）
- [ ] 个性化推荐（根据用户兴趣）
- [ ] 多平台发布（公众号、微博、Twitter）
- [ ] 评论互动分析
- [ ] 趋势预测
