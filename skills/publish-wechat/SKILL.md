---
name: publish-wechat
description: 读取news_translated.json，生成公众号HTML并发布到草稿箱
triggers:
  - 命令: publish news
  - 命令: 发布到公众号

# 输入文件
INPUT_FILE: "news_translated.json"

# 去重配置
DUPLICATE_FILE: "published_articles.json"

# 微信配置
WECHAT_APP_ID: "wxa87b65ba78d3c822"
WECHAT_APP_SECRET: "ac6a029c2b4ef7c1b89fbaeeaace3931"

---

# Publish WeChat Worker

## 功能
1. 读取 news_translated.json
2. 检查去重（比对 published_articles.json）
3. 生成微信公众号格式的 HTML
4. 发布到公众号草稿箱
5. 记录已发布文章到历史文件

## 执行命令

```bash
cd ~/Projects/llms/agent/ai-news

python3 publish_worker.py
```

## HTML 格式要求

### 1. 橙色头部
- 无emoji
- 格式：`<p style="...background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%)...>`
- 动态标题：早报/午报/晚报（根据北京时间）

### 2. 开场白
- 有科技感、有温度、不浮夸
- 不使用"炸裂！"等夸张词汇
- 每次角度不同，不要重复

### 3. 平台标题
- 居中展示（text-align: center）
- 🔥 只在 Hacker News 出现一次
- 颜色：Hacker News #ff6600, Product Hunt #da552f, TechCrunch #0a9900

### 4. 新闻条目
- 每条140字+
- 正文黑体（color: #333）
- 无URL
- 标题加粗（color: #1a1a1a）

### 5. 结尾
- 二维码: https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png
- 公众号名称：grepAI

## 检查清单
- [ ] 读取 news_translated.json 成功
- [ ] 检查去重
- [ ] 生成正确格式的 HTML
- [ ] 发布到公众号草稿箱
- [ ] 更新历史记录
- [ ] 打印发布统计