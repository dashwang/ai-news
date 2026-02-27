---
name: fetch-ai-news
description: 抓取北美AI新闻，翻译成中文，顶级记者风格编排，至少20条新闻，发布到微信公众号草稿箱
triggers:
  - 命令: fetch news
  - 命令: 抓取AI新闻
  - 命令: 发布AI新闻
  - 命令: AI News
---

# AI News 完整流程

当用户要求抓取并发布AI新闻时，执行以下完整流程：

## 核心要求：必须发布至少20条新闻！

**严格检查：**
- 如果新闻不足20条，继续抓取直到≥20条
- 每条新闻都要翻译成中文
- 不能遗漏任何新闻源

## API 基础信息

- **Railway URL**: `https://ai-news-production-2735.up.railway.app`

## Step 1: 调用 Railway 获取英文新闻

```bash
curl "https://ai-news-production-2735.up.railway.app/api/fetch"
```

返回数据后，检查 news 数量：
- 统计所有来源的新闻总数
- 如果不足20条，记录缺少的数量
- 继续抓取或重复调用直到满足20条

## Step 2: 翻译并编排（顶级记者风格）

### 新闻统计
- OpenAI: X条
- Hacker News: X条
- TechCrunch: X条
- 其他来源: X条
- 总计: 必须≥20条

### 标题技巧
- 用数字制造紧迫感：「突发」、「刚刚」、「重磅」
- 制造悬念：「竟然」、「没想到」、「太强了」
- 对话感：「炸锅了」、「彻底杀疯了」

### 内容编排公式
```
[开场白 - 制造焦虑/好奇]
[核心新闻1-10条 - 每条都要有]
[扩展新闻11-20条 - 继续填充]
[互动引导 - 评论/关注]
```

###  emoji 使用规范
- 🔥 热点新闻
- 💰 融资/财报
- 🤖 AI/科技
- 👀 争议/瓜
- 🚀 产品发布
- 💡 观点/洞察
- 📱 互联网
- 🏢 大公司

### 严格检查清单
- [ ] 总新闻数 ≥ 20
- [ ] 每条新闻都有中文标题
- [ ] 每条新闻都有中文摘要
- [ ] 格式统一美观
- [ ] 无英文残留

### HTML格式要求

```html
<p style="text-align: center; font-size: 22px; font-weight: bold;">🔥 2026.02.26 科技早报</p>
<p style="text-align: center; color: #888; font-size: 13px;">今日精选 · X条新闻</p>

<p><strong>🤖 OpenAI 动态 (X条)</strong></p>
<p>1. [新闻标题中文] - [摘要]</p>
<p>2. [新闻标题中文] - [摘要]</p>
<p>...</p>

<p><strong>🔥 Hacker News 热门 (X条)</strong></p>
<p>1. [新闻标题中文]</p>
<p>...</p>

<p><strong>📱 TechCrunch 科技 (X条)</strong></p>
<p>1. [新闻标题中文]</p>
<p>...</p>

<p style="text-align: center; margin-top: 20px;">📱 关注我们，获取每日科技前沿！</p>
```

## Step 3: 发布到微信公众号

```bash
curl -X POST "https://ai-news-production-2735.up.railway.app/api/publish_wechat" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [
      {
        "title": "🔥 2026.02.26 科技早报 | X条精选",
        "content": "生成的HTML（必须包含≥20条新闻）",
        "digest": "今日精选X条科技资讯",
        "source_url": "https://veray.ai"
      }
    ]}'
```

## 返回结果

告诉用户：
1. 成功抓取了 **X条新闻**（必须≥20）
2. 来源分布：OpenAI X条 + HackerNews X条 + TechCrunch X条
3. 已用顶级记者风格翻译编排
4. 已发布到微信公众号草稿箱
5. 提醒用户去公众号后台确认发布
