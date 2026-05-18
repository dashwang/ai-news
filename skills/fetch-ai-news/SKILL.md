---
name: fetch-ai-news
description: 抓取北美AI新闻，翻译成中文，编排后发布到微信公众号草稿箱
triggers:
  - 命令: fetch news
  - 命令: 抓取AI新闻
  - 命令: 发布AI新闻
  - 命令: AI News
  - 命令: ai news

# AI News 发布技能

## 发布流程

当用户喊 "AI News" 或类似命令时，执行以下流程：

### Step 1: 抓取新闻
```bash
cd ~/.openclaw/workspace/ai-news-backend && python3 fetch_news.py
```

### Step 2: 发布到公众号
```bash
cd ~/.openclaw/workspace/ai-news-backend && \
export WECHAT_APP_ID="wxa87b65ba78d3c822" && \
export WECHAT_APP_SECRET="ac6a029c2b4ef7c1b89fbaeeaace3931" && \
python3 publish_local.py
```

## 格式要求

### 头部
- 橙色渐变背景：`background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%)`
- 标题格式：`{日期} 全球AI科技{早报/午报/晚报}`
- 副标题：`{总条数}条精选速览`

### 平台板块（彩色边框背景）
- 🔥 Hacker News: 橙色 #ff6600 / #fff3e0
- 📱 TechCrunch: 绿色 #0a9900 / #e8f5e9
- 🚀 Product Hunt: 红色 #da552f / #fce4ec
- 💡 The Sequence / SubStack: 紫色 #6a1b9a / #f3e5f5
- 📡 Latent Space: 蓝色 #0288d1 / #e1f5fe
- 🔮 Exponential View: 深红 #c62828 / #ffebee

### 新闻条目
- 中文标题
- ❤️分数显示
- 每条一行，不要URL

### 结尾
- 引导语
- 二维码（180x180）
- 版权信息

## 新闻来源
- Hacker News
- TechCrunch
- Product Hunt
- TheSequence
- LatentSpace
- ExponentialView
- LexFridman
- LennysNewsletter

## 返回信息
告诉用户：成功条数、平台数、media_id