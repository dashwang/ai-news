---
name: 爆款单文
description: 根据热点快速生成1500字+的爆款公众号文章。先获取AI新闻热点，提供选项让用户选择，确认后写文发布
triggers:
  - 命令: 爆款单文
  - 命令: 写文章
  - 命令: 生成文章

# 爆款单文 Skill

当用户要求写一篇爆款公众号文章时，执行以下交互流程：

## 完整流程

### Step 1: 获取今日热点

先调用AI News API获取今日热点：
```bash
curl -s "https://ai-news-production-2735.up.railway.app/api/fetch?refresh=true"
```

### Step 2: 整理热点，给出选项

从新闻中提炼 3-5 个有话题性的选题，以列表形式呈现给用户：

```
📰 今日热点选项：

1. [热点标题1]
   - 关键词：xxx
   - 角度：xxx

2. [热点标题2]
   - 关键词：xxx
   - 角度：xxx

3. [热点标题3]
   - 关键词：xxx
   - 角度：xxx
```

### Step 3: 用户确认

等待用户回复选择的关键词或编号。

**用户可能：**
- 回复数字 "1"、"2"、"3"
- 回复修改后的关键词
- 提出自己的角度

### Step 4: 写文章

用户确认后：

1. **搜索素材** - 用 web_search/web_fetch 抓取相关原文
2. **翻译编辑** - 翻译成中文，扩展成 1500+ 字
3. **按照结构写作**：
   - 开头吸睛（100-200字）
   - 背景铺垫（200-300字）
   - 3个核心观点（每个300-400字）
   - 结尾引导（100-200字）
4. **highlight关键结论** - 用彩色背景突出

### Step 5: 发布到公众号

```bash
curl -X POST "https://ai-news-production-2735.up.railway.app/api/publish_wechat" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [{
      "title": "[标题]",
      "content": "[HTML内容]",
      "digest": "[摘要]",
      "source_url": "https://veray.ai"
    }]
  }'
```

## 写作规范

### 字数要求
- 总字数：1500字以上
- 每段话要有信息增量
- 避免车轱辘话

### 排版规范
```html
<!-- 标题 -->
<p style="text-align:center;font-size:24px;font-weight:bold;margin:20px">[标题]</p>

<!-- 章节 -->
<h3 style="margin:25px 20px 15px;color:#ff6600;font-size:18px">📌 章节标题</h3>

<!-- 重点 -->
<p style="margin:20px;background:#fff5f5;padding:15px;border-radius:8px"><strong>重点句子</strong></p>

<!-- 正文 -->
<p style="margin:20px;font-size:15px;line-height:1.8;color:#333">[内容]</p>

<!-- 结尾 -->
<p style="text-align:center;margin-top:30px;padding:20px;background:#fafafa"><strong>👍 觉得有用分享朋友</strong></p>
```

### 风格
- 科技、有温度、懂人性、不浮夸
- 适当用 emoji
- 关键结论高亮

## 返回格式

### 热点选项
```
🔥 今日AI热点选项：

1️⃣ [热点标题]
   关键词：xxx
   写作角度：xxx

2️⃣ [热点标题]
   关键词：xxx
   写作角度：xxx

3️⃣ [热点标题]
   关键词：xxx
   写作角度：xxx

请回复数字或关键词 ~
```

### 发布成功
```
✅ 已发布！

- 标题：xxx
- media_id：xxx

去公众号后台确认发布吧 ~
```
