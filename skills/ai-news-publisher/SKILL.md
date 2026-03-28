---
name: ai-news-publisher
description: 北美AI科技新闻抓取、编排与微信公众号发布完整工作流。包含去重、动态标题、热内容置顶、最终优化排版等核心功能。
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
3. **动态标题** - 根据当日热点生成吸引眼球的标题
4. **热内容置顶** - 标题对应的文章放全文最前
5. **最终优化排版** - 简洁专业，四区分色

## 最终排版规范（2026年3月28日优化版）

### 1. 热点聚焦模块（最重要内容）
- 白色背景 + 橙色边框（与下方区别开）
- 标题居中 + 橙色高亮
- 内容居中显示
- **必须是当日最热的AI新闻**

### 2. 四平台子标题（每个平台独立颜色）
- **HackerNews**: 橙色 #e65100，背景 #fff3e0
- **ProductHunt**: 粉色 #c2185b，背景 #fce4ec
- **SubStack**: 金色 #f57c00，背景 #fff8e1
- **TechCrunch**: 绿色 #2e7d32，背景 #e8f5e9

### 3. 文章标题和摘要格式（重要！）
- **标题必须是中文**，翻译自英文原文
- **每个文章块2-3行摘要**，不要太空
- 格式：数字序号 + 中文标题（链接）+ 2-3行中文摘要
- 标题用黑色加粗
- 摘要用深灰色 #555

### 4. 文章分割
- 虚线：border-top: 1px dashed #e0e0e0

### 5. 公众号信息
- 名称：grepAI
- 二维码：https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png
- 尺寸：180px

### 6. 头条格式
- 橙色渐变头部：linear-gradient(135deg, #ff6600 0%, #ff8533 100%)
- 文字：北美AI科技日报

## 发布检查清单

- [ ] 标题无emoji
- [ ] 无开场白（用户要求去掉）
- [ ] 每平台至少4篇新闻
- [ ] **每条新闻标题必须是中文**
- [ ] **每条摘要2-3行，不要太空**
- [ ] 热点聚焦放全文最前（白色背景+橙色边框）
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