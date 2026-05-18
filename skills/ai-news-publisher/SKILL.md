---
name: ai-news-publisher
description: AI科技新闻抓取与微信公众号排版。不含自动发布能力，需手动复制到公众号后台。
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

1. **多源抓取** - 使用 `web_fetch` 直接抓取（建议 HackerNews、TechCrunch RSS）
2. **智能热点选择** - 根据 points/comments 数选择置顶内容
3. **配图匹配** - 根据文章主题选择相关图片（Unsplash）
4. **公众号排版** - 生成可直接复制的排版内容

## ⚠️ 不含功能

- ~~外部 API 抓取~~（已移除，服务不稳定）
- ~~自动发布到微信公众号~~（无 API 能力）
- ~~去重~~（需手动）

## 排版规范（2026年3月28日最新版）

### 1. 热点聚焦模块（最重要！）
- **选择标准**：当日最具话题性的AI新闻
- 白色背景 + 橙色边框（与下方区别开）
- 标题居中 + 橙色高亮
- 内容居中显示

### 2. 模块顺序动态调整（重要！）
- **置顶文章对应的模块也要置顶**
- 例如：热点是SubStack的文章 → SubStack模块放到第一个
- **添加【置顶】标记**在模块标题后面，如：【置顶】SubStack
- 其他模块按默认顺序：HackerNews → ProductHunt → TechCrunch
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

## 快速开始（2026年4月更新）

### 抓取新闻（使用内置 web_fetch）

由于外部 API 服务不稳定，改为直接用 `web_fetch` 抓取：

```bash
# 抓取 HackerNews
web_fetch("https://news.ycombinator.com/")

# 抓取 TechCrunch AI
web_fetch("https://techcrunch.com/feed/")
```

### 手动抓取流程

1. 用 `web_fetch` 从以下来源抓取：
   - HackerNews: `https://news.ycombinator.com/`
   - TechCrunch: `https://techcrunch.com/category/artificial-intelligence/feed/`
   
2. 提取 AI 相关新闻，翻译标题和摘要

3. 按排版规范编排内容

4. 手动复制到公众号后台发布

### ⚠️ 已知限制

- ❌ 无微信公众号 API 自动发布能力
- ❌ ProductHunt 有反爬保护（403）
- ✅ 建议手动复制发布或配置第三方工具

## 相关文章

- [viral-article-writing](./viral-article-writing) - 爆款公众号文章写作指南
- [wechat-article-critic](./wechat-article-critic) - 公众号文章评审标准

## 安全建议

🔐 **不要在聊天中明文发送 credentials**  
如需配置 API keys，请使用：
```bash
openclaw configure --section web
```
或设置 Gateway 环境变量

---

## 更新日志

### 2026-04-01
- 移除挂掉的外部 API（Railway / Fly）
- 改用内置 `web_fetch` 直接抓取
- 明确标注：无自动发布能力
- 增加安全建议（credentials 处理）