---
name: fetch-ai-news
description: 抓取北美AI新闻，翻译成中文，编排后先写入飞书文档，再发布到微信公众号草稿箱
triggers:
  - 命令: fetch news
  - 命令: 抓取AI新闻
  - 命令: 发布AI新闻
  - 命令: AI News
  - 命令: ai news

# ✅ 2026.03.29 更新 - 本地直发版
# 不再依赖 Railway，后端直接跑在 ~/openclaw/workspace/ai-news-backend/

## 新闻源（4大平台）
- Hacker News: https://news.ycombinator.com/rss
- TechCrunch: https://techcrunch.com/feed/
- Product Hunt: https://www.producthunt.com/feed
- TheSequence / LatentSpace 等

## 去重配置
历史发布记录文件: ~/.openclaw/workspace/ai-news-backend/published_articles.json

## 关键格式要点
1. 每条新闻必须140字+
2. 4平台用不同颜色边框背景（不是纯色背景）
3. 正文黑体（color: #333)
4. 标题党一点，用 emoji
5. 不要URL
6. 写作风格：科技、有温度、懂人性、不浮夸
7. 🔥 只在Hacker News标题用一次
8. 橙色头部标题无emoji
9. 二维码URL: https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png
10. **去重：必须比对历史发布，避免重复**
11. **动态标题：每次根据当日热点生成**
12. 公众号名称：grepAI

## 格式检查清单

### 1. 橙色头部
- [ ] 无emoji（如📰、🔥）
- [ ] 格式：`<p style="...background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%)...>`
- [ ] 动态标题：早报/午报/晚报（根据北京时间）

### 2. 开场白
- [ ] 有科技感、有温度、不浮夸
- [ ] 不使用"炸裂！"等夸张词汇
- [ ] 每次角度不同，不要重复

### 3. 4个平台标题
- [ ] 居中展示（text-align: center）
- [ ] 🔥 只在Hacker News出现一次
- [ ] 颜色正确：Hacker News #ff6600, Product Hunt #da552f, TechCrunch #0a9900, SubStack #ff4400

### 4. 新闻条目
- [ ] 每条140字+
- [ ] 正文黑体（color: #333）
- [ ] 无URL
- [ ] 标题加粗（color: #1a1a1a）

### 5. 结尾
- [ ] 二维码URL: https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png
- [ ] 公众号名称：grepAI
- [ ] 有版权信息

---

# AI News 完整流程（本地直发版）

## Step 1: 抓取新闻

```bash
cd ~/.openclaw/workspace/ai-news-backend && python3 fetch_news.py
```

## Step 2: 发布到公众号

```bash
cd ~/.openclaw/workspace/ai-news-backend && \
export WECHAT_APP_ID="wxa87b65ba78d3c822" && \
export WECHAT_APP_SECRET="ac6a029c2b4ef7c1b89fbaeeaace3931" && \
python3 publish_local.py
```

## Step 3: 更新历史记录

发布成功后，记录到 published_articles.json

## 微信公众号凭证

已在代码中硬编码，无需额外配置：
- WECHAT_APP_ID: wxa87b65ba78d3c822
- WECHAT_APP_SECRET: ac6a029c2b4ef7c1b89fbaeeaace3931

## 封面图

自动从 GitHub 下载真实二维码并上传到微信服务器。

## 返回结果

告诉用户：
1. 成功抓取了 X 条新闻
2. ✅ 已发布到微信公众号草稿箱
3. media_id
4. 提醒用户去公众号后台确认发布
