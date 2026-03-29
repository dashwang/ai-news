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

## 排版规范（2026年3月29日最新版）

### 1. 热点聚焦模块（最重要！）
- **白色背景 + 橙色边框**，与下方区别开
- 标题居中 + 橙色高亮
- **动态标题：根据最热话题生成，不要只写日期**

### 2. 动态标题规则
- 格式：`炸裂！XXX` / `突发！XXX` / `刚刚，XXX`
- 围绕当日最热门的话题生成
- 不要写死成日期开头

### 3. 四平台子标题（每个平台独立颜色）
- **HackerNews**: 橙色 #e65100，背景 #fff3e0
- **ProductHunt**: 粉色 #c2185b，背景 #fce4ec
- **SubStack**: 金色 #f57c00，背景 #fff8e1
- **TechCrunch**: 绿色 #2e7d32，背景 #e8f5e9

### 4. 文章标题和摘要格式
- **标题必须是中文**（全部翻译，不要英文）
- **标题加粗黑体（使用strong标签）**
- **每条140字+摘要**
- 摘要用深灰色 #555

### 5. 文章分割
- 虚线：border-top: 1px dashed #e0e0e0
- **间距要小（margin: 8px 0）**

### 6. 子模块文章数量
- **每个子模块保持4-5篇文章**
- 不要多，也不要少

### 7. 二维码
- **必须上传到微信服务器获取media_id**
- **不要用外链**
- 尺寸：180px × 180px

### 8. 公众号信息
- 名称：grepAI
- 尺寸：180px

## 发布前自我检查清单（必须逐项核对）

- [ ] **动态标题**：不是日期开头，而是围绕最热话题生成
- [ ] **中文标题**：每条新闻标题都翻译成中文
- [ ] **热点聚焦**：白色背景 + 橙色边框（不是渐变橙色背景）
- [ ] **四平台各不同色**：HN橙/Product粉/SubStack金/TC绿
- [ ] **文章数量**：每个子模块4-5篇
- [ ] **虚线间距**：小一点（margin: 8px 0）
- [ ] **标题加粗**：strong + color:#1a1a1a
- [ ] **摘要140字+**：每条都要达到
- [ ] **二维码**：必须上传到微信服务器，不用外链
- [ ] **公众号名称**：grepAI
- [ ] **【置顶】标记**：置顶文章对应的模块添加

## 执行流程

### Step 1: 抓取新闻（本地执行）
```bash
cd ~/.openclaw/workspace/skills/ai-news-publisher && python3 fetch_news.py
```

### Step 2: 发布到公众号
```bash
cd ~/.openclaw/workspace/skills/ai-news-publisher && \
export WECHAT_APP_ID="wxa87b65ba78d3c822" && \
export WECHAT_APP_SECRET="ac6a029c2b4ef7c1b89fbaeeaace3931" && \
python3 publish_local.py
```

## 数据存储
- 数据库: `data/news.db`
- 历史记录: `data/published_articles.json`

## 返回信息
告诉用户：成功条数、平台数、media_id、热点头条