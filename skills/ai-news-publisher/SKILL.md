---
name: ai-news-publisher
description: 北美AI科技新闻抓取、编排与微信公众号发布完整工作流。包含去重、动态标题、热内容置顶、配图匹配等核心功能。
triggers:
  - 命令: fetch news
  - 命令: 抓取AI新闻
  - 命令: 发布AI新闻
  - 命令: AI News
  - 命令: 爆款文章

# AI News Publisher - 微信公众号AI新闻发布工作流

## 核心功能
1. 多源抓取 - HackerNews、ProductHunt、TechCrunch、SubStack
2. 智能去重 - 对比历史发布记录，避免重复
3. 动态热点选择 - 根据当日热点选择最具话题性的内容置顶
4. 热内容置顶 - 标题对应的文章放全文最前
5. 模块动态调整 - 置顶文章对应的模块放到第一个，添加【置顶】标记

## 排版规范（2026年3月28日最新版）

### 1. 热点聚焦模块（最重要！）
- **白色背景 + 橙色边框**，与下方区别开
- 标题居中 + 橙色高亮
- 内容居中显示

### 2. 四平台子标题（每个平台独立颜色）
- **HackerNews**: 橙色 #e65100，背景 #fff3e0
- **ProductHunt**: 粉色 #c2185b，背景 #fce4ec
- **SubStack**: 金色 #f57c00，背景 #fff8e1
- **TechCrunch**: 绿色 #2e7d32，背景 #e8f5e9

### 3. 文章标题和摘要格式
- **标题必须是中文**
- **标题加粗黑体（使用b标签）**
- **每条140字+摘要**
- 摘要用深灰色 #555

### 4. 文章分割
- 虚线：border-top: 1px dashed #e0e0e0

### 5. 公众号信息
- 名称：grepAI
- 二维码：https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png
- 尺寸：180px

## 发布检查清单
- [ ] 热点聚焦选择当日最具话题性的内容
- [ ] 标题无emoji
- [ ] 无开场白
- [ ] 每平台至少4篇新闻
- [ ] 每条新闻标题必须是中文
- [ ] 每条摘要140字+
- [ ] 四平台子标题各不同色
- [ ] 文章标题黑色加粗
- [ ] 虚线分割
- [ ] 公众号名称grepAI + 二维码180px
- [ ] 置顶文章对应的模块添加【置顶】标记

## 执行流程

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

## 返回信息
告诉用户：成功条数、平台数、media_id、热点头条