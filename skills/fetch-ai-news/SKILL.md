---
name: fetch-ai-news
description: 抓取北美AI新闻，翻译成中文，编排后先写入飞书文档，再发布到微信公众号草稿箱
triggers:
  - 命令: fetch news
  - 命令: 抓取AI新闻
  - 命令: 发布AI新闻
  - 命令: AI News
---

# AI News 完整流程

当用户要求抓取并发布AI新闻时，执行以下完整流程：

## 飞书文档配置

- **Doc Token**: `XMSudBIsUoGD20x7WKLctFCend9`
- 文档标题：「北美AI News」

## Step 1: 调用 Railway 获取英文新闻

```bash
curl "https://ai-news-production-2735.up.railway.app/api/fetch"
```

返回4个站点：HackerNews、LennysNewsletter、LexFridman、TechCrunch

## Step 2: 翻译并编辑

每条新闻需要展开140字以上的中文介绍。

## Step 3: 微信公众号排版（重要！）

### 开头模板（北美AI科技日报图）
```html
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); border-radius: 0;">
  <span style="font-size: 14px; color: #fff; opacity: 0.9;">📰 科技日报</span>
</p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">
  💰 2026.02.28 全球AI科技早报
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">
  今日精选 · 4个站点 · N条重磅新闻
</p>
```

### 4大部分样式（带Logo+配色）
```html
<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600;">
  <strong style="font-size: 16px; color: #ff6600;">🔥 Hacker News 热门</strong>
</p>
```

| 平台 | 颜色 | emoji |
|------|------|-------|
| Hacker News | #ff6600 | 🔥 |
| LennysNewsletter | #ff4400 | 💡 |
| LexFridman | #1a1a1a | 🎙️ |
| TechCrunch | #0a9900 | 📱 |

### 结尾模板（导流微信二维码）
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

<p style="text-align: center; margin-top: 20px; font-size: 13px; color: #999; line-height: 1.6;">
  💬 欢迎评论交流，说说你的看法
</p>
<p style="text-align: center; margin-top: 15px; font-size: 11px; color: #ccc; letter-spacing: 1px;">
  © 2026 科技日报 | 认真做内容
</p>
```

### 新闻条目格式（不要URL）
```html
<p style="margin: 15px 0 5px 0;">
  <strong style="font-size: 15px; color: #1a1a1a;">1. 新闻标题</strong>
</p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">
  140字以上的中文展开介绍...
</p>
<p style="margin: 5px 0 15px 0; border-bottom: 1px dashed #eee;"></p>
```

## Step 4: 写入飞书文档

```json
{
  "action": "update_block",
  "doc_token": "XMSudBIsUoGD20x7WKLctFCend9",
  "block_id": "BnJjdiIProug5Lx8vJKc2M9YnTh",
  "content": "完整Markdown内容..."
}
```

## Step 5: 发布到微信公众号草稿箱

```bash
curl -X POST "https://ai-news-production-2735.up.railway.app/api/publish_wechat" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [{
      "title": "2026.02.28 全球AI科技早报",
      "content": "<完整HTML内容 include 开头+结尾>",
      "digest": "今日精选全球AI科技资讯",
      "source_url": "https://veray.ai"
    }]
  }'
```

## 返回结果

告诉用户：
1. 成功抓取了 X 条新闻（来自4个站点）
2. 已翻译并编辑完成，每条140字+展开介绍
3. ✅ 已写入飞书文档「北美AI News」
4. ✅ 已发布到微信公众号草稿箱
5. 提醒用户去公众号后台确认发布
