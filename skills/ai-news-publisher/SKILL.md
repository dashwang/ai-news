---
name: ai-news-publisher
description: 北美AI科技新闻抓取、编排与微信公众号发布完整工作流。包含去重、动态标题、热内容置顶、配图匹配等核心功能。
triggers:
  - 命令: fetch news
  - 命令: 抓取AI新闻
  - 命令: 发布AI新闻
  - 命令: AI News
  - 命令: 爆款文章
---

# AI News Publisher - 微信公众号AI新闻发布工作流

## 概述

本技能实现从北美AI科技新闻抓取、编辑、排版到微信公众号发布的完整自动化流程。

## 核心功能

1. **多源抓取** - HackerNews、ProductHunt、TechCrunch、SubStack
2. **智能去重** - 对比历史发布记录，避免重复
3. **动态热点选择** - 根据当日热点选择最具话题性的内容置顶
4. **热内容置顶** - 标题对应的文章放全文最前
5. **配图匹配** - 根据文章主题选择相关图片，而非随机

## 排版规范（2026年3月28日最新版）

### 1. 热点聚焦模块（最重要！）
- **选择标准**：当日最具话题性的AI新闻
- 白色背景 + 橙色边框（与下方区别开）
- 标题居中 + 橙色高亮
- 内容居中显示
- **示例**：Latent Space的"一切皆为CLI"是今天的热点

### 2. 四平台子标题（每个平台独立颜色）
- **HackerNews**: 橙色 #e65100，背景 #fff3e0
- **ProductHunt**: 粉色 #c2185b，背景 #fce4ec
- **SubStack**: 金色 #f57c00，背景 #fff8e1
- **TechCrunch**: 绿色 #2e7d32，背景 #e8f5e9

### 3. 文章标题和摘要格式
- **标题必须是中文**，翻译自英文原文
- **标题加粗黑体**（使用<b>标签）
- **每个文章块140字+摘要**，不要太空
- 摘要用深灰色 #555

### 4. 配图选择规则（重要！）
- **不要随机生成配图**
- 根据文章主题选择相关图片：
  - CLI/Terminal主题 → 终端/命令行图片
  - NVIDIA/GPU主题 → 芯片/服务器图片
  - 自动驾驶/Waymo主题 → 汽车/无人车图片
  - AI Agent主题 → 机器人/代码图片
- 推荐图片源：Unsplash（可商用）

### 5. 文章分割
- 虚线：border-top: 1px dashed #e0e0e0

### 6. 公众号信息
- 名称：grepAI
- 二维码：https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png
- 尺寸：180px

## 发布检查清单

- [ ] 热点聚焦选择当日最具话题性的内容
- [ ] 标题无emoji
- [ ] 无开场白
- [ ] 每平台至少4篇新闻
- [ ] 每条新闻标题必须是中文
- [ ] 每条摘要2-3行，不要太空
- [ ] **配图与文章主题相关**
- [ ] 四平台子标题各不同色
- [ ] 文章标题黑色加粗
- [ ] 虚线分割
- [ ] 公众号名称grepAI + 二维码180px

## 快速开始

```bash
# 抓取并发布AI新闻
curl "https://ai-news-production-2735.up.railway.app/api/fetch"
```

## 相关文章

- [viral-article-writing](./viral-article-writing) - 爆款公众号文章写作指南
- [wechat-article-critic](./wechat-article-critic) - 公众号文章评审标准