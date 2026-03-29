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

在生成文章时，必须严格遵循以下从上到下的模块结构与样式规范：

### 1. 顶部日期横幅 (Daily Banner)
- **视觉表现**：橙色背景的圆角矩形块
- **内容要求**：
  - 第一行：固定文字「北美AI科技日报」，居中，大号加粗字体，白色
  - 第二行：当天的日期（如「2026年3月29日」），居中，标准字体，白色
- **HTML示例**：
```html
<p style="margin: 15px; padding: 20px; background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); border-radius: 12px; text-align: center;">
  <strong style="font-size: 20px; color: #fff;">北美AI科技日报</strong>
  <br><span style="font-size: 14px; color: #fff;">2026年3月29日</span>
</p>
```

### 2. 核心摘要框 (Highlight Summary Box)
- **视觉表现**：白色背景，外圈带有橙色圆角边框
- **内容要求**：
  - 摘要标题：提炼当日最具爆炸性的1-2个新闻组合成一句话标题，居中显示
  - 关键信息（如品牌名、重大事件）需使用橙色字体高亮
  - 摘要正文：用一段话（约100-150字）连贯地概述标题中提到的核心事件及其行业影响
  - 文字颜色为浅灰色，排版整齐
- **HTML示例**：
```html
<p style="margin: 15px; padding: 20px; background: #fff; border: 3px solid #ff6600; border-radius: 12px; text-align: center;">
  <strong style="font-size: 18px; color: #ff6600;">扎克伯格主动联系马斯克</strong>
</p>
<p style="margin: 0 20px 20px 20px; font-size: 14px; color: #888; line-height: 1.8; text-align: justify;">摘要正文内容...</p>
```

### 3. 板块标题 (Section Header)
- **视觉表现**：浅灰色/米色矩形背景块，左侧带有粗橙色边带
- **内容要求**：板块名称（如「HackerNews」「Product Hunt」），使用橙色字体并加粗
- **HTML示例**：
```html
<p style="margin: 20px 0 10px 0; padding: 10px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #e65100; text-align: center;">
  <strong style="font-size: 15px; color: #e65100;">HackerNews</strong>
</p>
```

### 4. 资讯列表 (News Items)
- **视觉表现**：列表式排版，条目之间有虚线分隔
- **内容要求**：
  - 标题格式：使用加粗字体，中文标题
  - 正文解读：对新闻进行中文编译和解读，140字+
  - 分割线：每条新闻结束后，插入一条细虚线作为条目分割
- **HTML示例**：
```html
<p style="margin: 12px 0 3px 0;"><strong style="font-size: 14px; color: #1a1a1a;">标题</strong></p>
<p style="margin: 0; font-size: 13px; color: #555; line-height: 1.7; text-align: justify;">正文内容...</p>
<p style="margin: 8px 0; border-top: 1px dashed #e0e0e0;"></p>
```

### 5. SubStack整合模块
- 所有SubStack来源（TheSequence、LatentSpace、LexFridman、Lenny's Newsletter等）合并为一个「SubStack 精选」模块
- 模块标题：金色边框，文字「SubStack 精选」

### 6. 四平台颜色配置
- **HackerNews**: 橙色 #e65100，背景 #fff3e0
- **ProductHunt**: 粉色 #c2185b，背景 #fce4ec
- **SubStack**: 金色 #f57c00，背景 #fff8e1
- **TechCrunch**: 绿色 #2e7d32，背景 #e8f5e9

### 7. 二维码
- **必须上传到微信服务器获取media_id**
- **不要用外链**
- 尺寸：180px × 180px
- 放在文章底部

### 8. Emoji规范
- **标题和正文中禁止出现任何emoji字符**

## 发布前自我检查清单（14项）

- [ ] **顶部横幅**：橙色背景 + 「北美AI科技日报」+ 日期
- [ ] **核心摘要框**：白色背景 + 橙色边框，标题高亮关键词
- [ ] **板块标题**：浅色背景 + 橙色左边框，平台名橙色加粗
- [ ] **资讯列表**：序号格式 + 虚线分割
- [ ] **中文标题**：每条新闻标题都翻译成中文
- [ ] **无emoji**：标题和正文中禁止任何emoji字符
- [ ] **四平台各不同色**：HN橙/Product粉/SubStack金/TC绿
- [ ] **文章数量**：每个子模块4-5篇
- [ ] **标题加粗**：strong + color:#1a1a1a
- [ ] **摘要140字+**：每条都要达到
- [ ] **二维码**：必须上传到微信服务器
- [ ] **公众号名称**：grepAI
- [ ] **SubStack整合**：合并为一个模块
- [ ] **不重复**：已置顶的新闻不再重复显示

## 数据存储
- 数据库: `data/news.db`
- 历史记录: `data/published_articles.json`

## 返回信息
告诉用户：成功条数、平台数、media_id