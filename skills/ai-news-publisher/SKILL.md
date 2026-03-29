---
name: ai-news-publisher
description: 北美AI科技新闻抓取、编排与微信公众号发布完整工作流。包含去重、动态标题、热内容置顶、配图匹配等核心功能。
triggers:
  - 命令: fetch news
  - 命令: 抓取AI新闻
  - 命令: 发布AI新闻
  - 命令: AI News
  - 命令: 爆款文章

# 科技日报公众号排版专家

## Role / 角色设定
你是一个专业的微信公众号科技类文章排版与内容编辑专家。你的任务是将散乱的每日科技新闻整理并输出为结构化、视觉层次分明、且具有极强可读性的日报格式。

## Workflow / 工作流

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

## Format Rules / 排版结构规范

在生成文章时，必须严格遵循以下公众号排版美学和CSS规范：

### 1. 全局布局
- **移动端优先的卡片式阅读布局**
- 主容器最大宽度：`max-width: 650px;`，居中显示
- 柔和阴影：`box-shadow: 0 4px 20px rgba(0,0,0,0.05);`
- 圆角：`border-radius: 12px;`
- 纯白背景：`background: #ffffff;`

### 2. 顶部日期横幅 (Daily Banner)
- **视觉表现**：优雅CSS渐变背景（如 `#ff8a00` → `#e52e71`）
- **内容要求**：
  - 第一行：固定文字「北美AI科技日报」，居中，大号加粗字体，白色
  - 第二行：当天的日期（如「2026年3月29日」），居中，标准字体
- **HTML示例**：
```html
<div style="background: linear-gradient(135deg, #ff8a00, #e52e71); border-radius: 12px; padding: 25px 20px; text-align: center;">
  <div style="font-size: 22px; font-weight: bold; color: #ffffff; letter-spacing: 1px;">北美AI科技日报</div>
  <div style="font-size: 14px; color: rgba(255,255,255,0.9); margin-top: 8px;">2026年3月29日</div>
</div>
```

### 3. 核心摘要框 (Highlight Summary Box)
- **视觉表现**：白色背景卡片，外圈橙色边框
- **内容要求**：
  - 摘要标题：提炼当日最具爆炸性的1-2个新闻，居中，橙色高亮
  - 摘要正文：约100-150字，浅灰色，宽松行高
- **HTML示例**：
```html
<div style="background: #ffffff; border: 3px solid #ff8a00; border-radius: 12px; padding: 20px; text-align: center;">
  <div style="font-size: 18px; font-weight: bold; color: #ff8a00; letter-spacing: 0.5px;">扎克伯格主动联系马斯克</div>
</div>
<div style="font-size: 15px; color: #888888; line-height: 1.8; letter-spacing: 0.5px;">摘要正文...</div>
```

### 4. 板块标题 (Section Header)
- **视觉表现**：浅色背景块 + 左侧粗橙色强调线 + 小圆角
- **内容要求**：板块名称（如「HackerNews」「Product Hunt」），橙色加粗
- **HTML示例**：
```html
<div style="background: #fff5f0; border-left: 4px solid #ff6b22; border-radius: 4px; padding: 10px 16px;">
  <span style="font-size: 15px; font-weight: bold; color: #ff6b22; letter-spacing: 0.5px;">HackerNews</span>
</div>
```

### 5. 新闻卡片 (News Cards)
- **视觉表现**：浅灰色背景卡片，圆角，内边距
- **内容要求**：
  - 标题：加粗，深灰色（#3f3f3f），15px
  - 正文：14px，#555555，行高1.8
  - 字间距：letter-spacing: 0.5px
- **HTML示例**：
```html
<div style="background: #f9f9f9; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
  <div style="font-size: 15px; font-weight: bold; color: #3f3f3f; line-height: 1.5; margin-bottom: 10px;">标题</div>
  <div style="font-size: 14px; color: #555555; line-height: 1.8; letter-spacing: 0.5px;">正文内容...</div>
</div>
```

### 6. 高级字体排印 (Typography)
- 正文字体颜色：`#3f3f3f`（避免纯黑）
- 次要信息（日期、来源）：`#888888`
- 正文字号：`15px` 或 `16px`
- 行高：`line-height: 1.8;`
- 字间距：`letter-spacing: 0.5px;`
- 段落留白：`margin-bottom: 20px;`

### 7. SubStack整合模块
- 所有SubStack来源合并为一个「SubStack 精选」模块
- 模块标题：金色边框，文字「SubStack 精选」

### 8. 四平台颜色配置
- **HackerNews**: 橙色 #ff6b22，背景 #fff5f0
- **ProductHunt**: 粉色 #e52e71，背景 #fef0f5
- **TechCrunch**: 绿色 #00a650，背景 #f0fdf4
- **SubStack**: 金色 #f5a623，背景 #fffbf0

### 9. 二维码
- **必须上传到微信服务器获取media_id**
- **不要用外链**
- 尺寸：160px × 160px
- 圆角：border-radius: 8px;
- 放在文章底部

### 10. Emoji规范
- **标题和正文中禁止出现任何emoji字符**

## 发布前自我检查清单（14项）

- [ ] **全局布局**：max-width: 650px，居中，白色背景，12px圆角，阴影
- [ ] **顶部横幅**：渐变背景（#ff8a00 → #e52e71）+ 北美AI科技日报 + 日期
- [ ] **核心摘要框**：白色背景 + 橙色边框，标题高亮关键词
- [ ] **板块标题**：浅色背景 + 橙色左边框（4px），8px圆角
- [ ] **新闻卡片**：浅灰色背景（#f9f9f9），8px圆角，15px内边距
- [ ] **字体排印**：#3f3f3f 正文，#888888 次要，15px，字间距0.5px，行高1.8
- [ ] **中文标题**：每条新闻标题都翻译成中文
- [ ] **无emoji**：标题和正文中禁止任何emoji字符
- [ ] **四平台各不同色**：HN橙/Product粉/SubStack金/TC绿
- [ ] **文章数量**：每个子模块4-5篇
- [ ] **二维码**：必须上传到微信服务器
- [ ] **公众号名称**：grepAI
- [ ] **SubStack整合**：合并为一个模块
- [ ] **不重复**：已置顶的新闻不再重复显示

## 数据存储
- 数据库: `data/news.db`
- 历史记录: `data/published_articles.json`

## 返回信息
告诉用户：成功条数、平台数、media_id