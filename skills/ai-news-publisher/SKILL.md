# AI News Publisher - 自动抓取翻译发布

## 概述

自动抓取 AI 新闻，翻译整理成公众号文章并发布。

## 数据源（4大平台）

1. **Hacker News** - `https://news.ycombinator.com/rss`
2. **SubStack (Lex Fridman + Lenny's Newsletter)** - `https://lexfridman.com/feed/` + `https://www.lennysnewsletter.com/feed`
3. **TechCrunch** - `https://techcrunch.com/feed/`
4. **Product Hunt** - `https://www.producthunt.com/feed`

## 微信公众号排版标准

### 封面区域 - Hacker News 橙黑风格

```html
<!-- 封面：橙黑科技风 -->
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); border-radius: 0;">
  <span style="font-size: 14px; color: #fff; opacity: 0.9;">📰 科技日报</span>
</p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">
  💰 1100亿美元！AI史上最大融资诞生
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">
  OpenAI估值7300亿美元，Anthropic硬刚五角大楼
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

### 结尾模板 - 温暖科技风（不要AI感）

```html
<!-- 结尾：温暖、真人感、科技感 + 公众号二维码 -->
<p style="text-align: center; margin-top: 30px; padding: 25px 20px; background: #fafafa; border-radius: 12px; border: 1px solid #eee;">
  <span style="font-size: 16px; color: #333; font-weight: 500;">
    👍 觉得有用？不妨分享给朋友 👏
  </span>
</p>

<!-- 公众号二维码 -->
<p style="text-align: center; margin-top: 20px;">
  <img src="https://mp.weixin.qq.com/cgi-bin/qrcode?action=download_searchlogo&token=640524074&lang=zh_CN" 
       style="width: 120px; height: 120px; border-radius: 8px;" 
       alt="科技日报公众号">
</p>
<p style="text-align: center; margin-top: 10px; font-size: 13px; color: #666;">
  📱 扫码关注「科技日报」<br>
  每天早上8点自动送达
</p>

<p style="text-align: center; margin-top: 20px; font-size: 13px; color: #999; line-height: 1.6;">
  💬 欢迎评论交流，说说你的看法
</p>
<p style="text-align: center; margin-top: 15px; font-size: 11px; color: #ccc; letter-spacing: 1px;">
  © 2026 科技日报 | 认真做内容
</p>
```

## 完整示例

```html
<!-- 封面 -->
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); border-radius: 0;">
  <span style="font-size: 14px; color: #fff; opacity: 0.9;">📰 科技日报</span>
</p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">
  💰 1100亿美元！AI史上最大融资诞生
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">
  OpenAI估值7300亿美元，Anthropic硬刚五角大楼
</p>

<!-- Hacker News -->
<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600;">
  <strong style="font-size: 16px; color: #ff6600;">🔥 Hacker News 热门</strong>
</p>

<p style="margin: 15px 0 5px 0;">
  <strong style="font-size: 15px; color: #1a1a1a;">1. Anthropic CEO硬刚五角大楼：拒绝向军方开放AI</strong>
</p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">
  Dario Amodei明确表示问心无愧地拒绝五角大楼要求...
</p>
<p style="margin: 5px 0 15px 0; border-bottom: 1px dashed #eee;"></p>

<!-- 其他平台... -->

<!-- 结尾 -->
<p style="text-align: center; margin-top: 30px; padding: 25px 20px; background: #fafafa; border-radius: 12px; border: 1px solid #eee;">
  <span style="font-size: 16px; color: #333; font-weight: 500;">
    👍 觉得有用？不妨分享给朋友 👏
  </span>
</p>

<!-- 公众号二维码 -->
<p style="text-align: center; margin-top: 20px;">
  <img src="https://mp.weixin.qq.com/cgi-bin/qrcode?action=download_searchlogo&token=640524074&lang=zh_CN" 
       style="width: 120px; height: 120px; border-radius: 8px;" 
       alt="科技日报公众号">
</p>
<p style="text-align: center; margin-top: 10px; font-size: 13px; color: #666;">
  📱 扫码关注「科技日报」<br>
  每天早上8点自动送达
</p>

<p style="text-align: center; margin-top: 20px; font-size: 13px; color: #999; line-height: 1.6;">
  💬 欢迎评论交流，说说你的看法
</p>
<p style="text-align: center; margin-top: 15px; font-size: 11px; color: #ccc; letter-spacing: 1px;">
  © 2026 科技日报 | 认真做内容
</p>
```

## 开头模板库（温暖科技风）

### 模板1：数字吸睛
```html
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); border-radius: 0;">
  <span style="font-size: 14px; color: #fff; opacity: 0.9;">📰 科技日报</span>
</p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">
  💰 1100亿美元！AI史上最大融资诞生
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">
  OpenAI估值7300亿美元，Anthropic硬刚五角大楼
</p>
```

### 模板2：话题吸睛
```html
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); border-radius: 0;">
  <span style="font-size: 14px; color: #fff; opacity: 0.9;">📰 科技日报</span>
</p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">
  ❓ 当AI巨头遇上五角大楼，会发生什么？
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">
  Dario Amodei硬刚五角大楼，AI行业迎来关键时刻
</p>
```

### 模板3：新闻联播风
```html
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); border-radius: 0;">
  <span style="font-size: 14px; color: #fff; opacity: 0.9;">📰 科技日报</span>
</p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">
  🔥 2026.02.27 科技圈发生了什么？
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">
  这一周的科技圈，信息量有点大
</p>
```

## 结尾模板库（温暖真人感）

### 模板1：互动引导 + 公众号二维码
```html
<p style="text-align: center; margin-top: 30px; padding: 25px 20px; background: #fafafa; border-radius: 12px; border: 1px solid #eee;">
  <span style="font-size: 16px; color: #333; font-weight: 500;">
    👍 觉得有用？不妨分享给朋友 👏
  </span>
</p>

<p style="text-align: center; margin-top: 20px;">
  <img src="https://mp.weixin.qq.com/cgi-bin/qrcode?action=download_searchlogo&token=640524074&lang=zh_CN" 
       style="width: 120px; height: 120px; border-radius: 8px;" 
       alt="科技日报公众号">
</p>
<p style="text-align: center; margin-top: 10px; font-size: 13px; color: #666;">
  📱 扫码关注「科技日报」<br>
  每天早上8点自动送达
</p>
```

### 模板2：关注引导
```html
<p style="text-align: center; margin-top: 30px; padding: 25px 20px; background: #fafafa; border-radius: 12px; border: 1px solid #eee;">
  <span style="font-size: 15px; color: #666;">
    📱 每天8点 | 点关注不迷路<br>
    💬 评论区聊聊，你最关注哪条？
  </span>
</p>
```

### 模板3：简洁有力
```html
<p style="text-align: center; margin-top: 30px; padding: 20px; background: #f5f5f5; border-radius: 8px;">
  <span style="font-size: 15px; color: #555;">
    👍 认同就分享 | 💬 评论区见
  </span>
</p>
```

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
