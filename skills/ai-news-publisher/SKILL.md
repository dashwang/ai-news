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

- `logo-hackernews.png` - Hacker News logo
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

### 顶级科技新闻开头模板

```html
<!-- 开头：制造紧迫感 + 话题性 -->
<p style="text-align: center; font-size: 20px; font-weight: bold; color: #e74c3c; margin-bottom: 10px;">
  📢 刚刚，AI行业又发生了一件大事！
</p>
<p style="text-align: center; font-size: 24px; font-weight: bold; color: #1a1a1a; margin-bottom: 8px;">
  🔥 2026.02.27 科技圈炸了
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin-bottom: 20px;">
  OpenAI刷新融资纪录，Anthropic硬刚五角大楼，AI格局巨变！
</p>
```

### 4大部分样式（带Logo+配色）

```html
<!-- 分区标题 -->
<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600;">
  <strong style="font-size: 16px; color: #ff6600;">🔥 Hacker News 热门</strong>
</p>
```

### 平台颜色主题

| 平台 | 颜色 | emoji |
|------|------|-------|
| Hacker News | #ff6600 | 🔥 |
| SubStack | #ff4400 | 💡 |
| TechCrunch | #0a9900 | 📱 |
| Product Hunt | #da552f | 🚀 |

### 单条新闻样式（140字左右）

```html
<p style="margin: 15px 0 5px 0;">
  <strong style="font-size: 15px; color: #1a1a1a;">1. 新闻标题</strong>
</p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">
  新闻内容...（140字左右）
</p>
<p style="margin: 5px 0 15px 0; border-bottom: 1px dashed #eee;"></p>
```

### 顶级科技新闻结尾模板

```html
<!-- 结尾：互动引导 + 紧迫感 -->
<p style="text-align: center; margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px;">
  <span style="font-size: 18px; color: #fff; font-weight: bold;">🚀 觉得有用？分享给朋友一起看！</span>
</p>
<p style="text-align: center; margin-top: 15px; font-size: 14px; color: #999;">
  📱 每天8点准时更新 | 点关注不迷路
</p>
<p style="text-align: center; margin-top: 10px; font-size: 12px; color: #ccc;">
  © 2026 科技日报 | 侵权必究
</p>
```

## 完整示例

```html
<p style="text-align: center; font-size: 20px; font-weight: bold; color: #e74c3c; margin-bottom: 10px;">
  📢 刚刚，AI行业又发生了一件大事！
</p>
<p style="text-align: center; font-size: 24px; font-weight: bold; color: #1a1a1a; margin-bottom: 8px;">
  🔥 2026.02.27 科技圈炸了
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin-bottom: 20px;">
  OpenAI刷新融资纪录，Anthropic硬刚五角大楼，AI格局巨变！
</p>

<!-- Hacker News -->
<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600;">
  <strong style="font-size: 16px; color: #ff6600;">🔥 Hacker News 热门</strong>
</p>

<p style="margin: 15px 0 5px 0;">
  <strong style="font-size: 15px; color: #1a1a1a;">1. Anthropic CEO硬刚五角大楼：拒绝向军方开放AI</strong>
</p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">
  Dario Amodei明确表示问心无愧地拒绝五角大楼要求，向军方无条件开放AI系统的要求，与OpenAI此前的类似争议形成呼应，引发关于AI伦理与国家安全边界的大讨论。
</p>
<p style="margin: 5px 0 15px 0; border-bottom: 1px dashed #eee;"></p>

<!-- 其他平台... -->

<!-- 结尾 -->
<p style="text-align: center; margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px;">
  <span style="font-size: 18px; color: #fff; font-weight: bold;">🚀 觉得有用？分享给朋友一起看！</span>
</p>
<p style="text-align: center; margin-top: 15px; font-size: 14px; color: #999;">
  📱 每天8点准时更新 | 点关注不迷路
</p>
```

## 开头模板库

### 模板1：震惊体
```html
<p style="text-align: center; font-size: 20px; font-weight: bold; color: #e74c3c; margin-bottom: 10px;">
  📢 刚刚，AI行业又发生了一件大事！
</p>
```

### 模板2：数字体
```html
<p style="text-align: center; font-size: 20px; font-weight: bold; color: #e74c3c; margin-bottom: 10px;">
  💰 1100亿美元！AI史上最大融资诞生
</p>
```

### 模板3：提问体
```html
<p style="text-align: center; font-size: 20px; font-weight: bold; color: #e74c3c; margin-bottom: 10px;">
  ❓ 当AI巨头遇上五角大楼，会发生什么？
</p>
```

## 结尾模板库

### 模板1：互动引导
```html
<p style="text-align: center; margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px;">
  <span style="font-size: 18px; color: #fff; font-weight: bold;">🚀 觉得有用？分享给朋友一起看！</span>
</p>
```

### 模板2：关注引导
```html
<p style="text-align: center; margin-top: 30px; padding: 15px; background: #f5f5f5; border-radius: 8px;">
  <span style="font-size: 16px;">📱 点关注，不错过每天科技热点！</span>
</p>
```

### 模板3：行动号召
```html
<p style="text-align: center; margin-top: 30px;">
  <span style="display: inline-block; padding: 12px 30px; background: #07c160; color: #fff; font-size: 16px; font-weight: bold; border-radius: 25px;">
    👍 点赞 + 📤 分享 + ❤️ 关注
  </span>
</p>
```

## 常见问题

1. **Railway 500 错误** - 检查 RSS 源是否有效
2. **微信 IP 白名单** - 需要在微信开放平台添加 Railway 服务器 IP（注意：Railway IP 会动态变化）
3. **新闻不足20条** - 需要检查各 RSS 源是否正常返回数据

## 后续迭代方向

- [ ] 增加更多新闻源
- [ ] 自动翻译（接入翻译API）
- [ ] 个性化推荐（根据用户兴趣）
- [ ] 多平台发布（公众号、微博、Twitter）
- [ ] 评论互动分析
- [ ] 趋势预测
- [ ] A/B测试不同开头/结尾效果
