---
name: ai-news-publisher
description: AI科技新闻抓取与微信公众号排版。5个核心源，各≥5条新闻。
triggers:
  - command: AI新闻
  - command: 抓取AI新闻
  - command: 北美AI圈日报
  - command: ai news
  - command: fetch ai news
---

# AI News Publisher - 智能新闻抓取与发布

## 概述

从5个核心AI新闻源实时抓取热点新闻，自动生成排版好的微信公众号文章，支持一键发布草稿。

## 核心功能

1. **多源抓取** - 5个源各≥5条（HN、TechCrunch、Latent Space、The Decoder、MIT Tech Review）
2. **热点选择** - 根据热度（score）自动选择头条
3. **公众号排版** - 清爽风格HTML（无外框、紧凑行距）
4. **草稿发布** - 自动创建公众号草稿（需配置AppID/Secret）

## 使用方法

```bash
cd /root/.openclaw/workspace/skills/ai-news-publisher

# 抓取并生成日报（不发布）
node fetch_news.js

# 生成并发布到公众号草稿箱
node fetch_news.js --publish
```

通过对话说：
- "AI新闻"
- "抓取AI新闻"
- "北美AI圈日报"

## 数据源（5个，各≥5条）

| 源 | 类型 | 接口 |
|----|------|------|
| Hacker News | Algolia API | ≥5条 |
| TechCrunch AI | RSS | ≥5条 |
| Latent Space | RSS | ≥5条 |
| The Decoder | RSS | ≥5条 |
| MIT Technology Review | RSS | ≥5条 |

**总计**：25条真实新闻

## 输出文件

```
ai-news-publisher/data/
├── news-2026-04-27.json        # 原始数据
├── wechat-html-2026-04-27.html # 排版HTML
└── published.json              # 发布记录
```

## 环境变量

```bash
export WECHAT_APP_ID="wxa87b65ba78d3c822"
export WECHAT_APP_SECRET="ac6a029c2b4ef7c1b89fbaeeaace3931"
```

## 发布流程

1. 抓取新闻 → `fetch_news.js`
2. 生成HTML → 自动生成 `data/wechat-html-*.html`
3. 发布草稿 → `--publish` 参数调用微信API
4. 手动确认 → 登录 mp.weixin.qq.com 点击发布（订阅号限制）

## 技术细节

- 零依赖：原生 Node.js，无需 npm install
- 纯前端抓取：直接 HTTP 请求
- 翻译：预填充中文字段（由助手提供，无需外部API）
- 容错：单源失败不影响整体

## 限制

- 订阅号无法自动发布（需手动确认）
- 服务号可自动发布（需认证权限）
