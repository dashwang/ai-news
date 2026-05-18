---
name: ai-hot-article
description: 抓取AI热点新闻，选TOP1写爆款深度文章（对标量子位/机器之心），用wechat-article-critic评审修改，发布到微信公众号
triggers:
  - 命令: 写热点文章
  - 命令: AI热点
  - 命令: 发布爆款
  - 命令: 深度文章

# AI热点文章完整流程（第三版 - 严格版）

当用户要求抓取热点、写深度文章、评审修改、发布时，执行以下完整流程：

## Step 1: 抓取AI新闻

调用Railway API获取最新AI新闻：
```bash
curl -s "https://ai-news-production-2735.up.railway.app/api/fetch"
```

## Step 2: 选出TOP1热点

选择标准：
1. 突破性进展
2. 重磅发布
3. 反直觉新闻
4. 行业大新闻

## Step 3: 写深度爆款文章（严格版）

### 写作要求

1. **主线清晰**：只有一个核心论点，所有板块围绕它展开
2. **字数**：1500-2500字
3. **深度**：不只是讲What，要讲Why + So What
4. **观点**：每个板块要有观点输出，不是罗列事实
5. **结构**：按"现象→原因→影响→数据→预测→行动"逻辑递进
6. **开头**：3句话内必须出现核心观点，标题就是观点
7. **配图**：有数据表格
8. **排版**：
   - 段落不超过3行
   - 多级标题
   - 重点句子加粗或单独成段

### 禁止事项
- ❌ 多个话题并列，没有核心论点
- ❌ 板块之间没有逻辑衔接
- ❌ 开头"XXXX年X月发布了..."
- ❌ 只有陈述，没有判断

## Step 4: 用wechat-article-critic评审

评审标准：

| 检查项 | 要求 |
|--------|------|
| 主线 | 只有一个核心论点 |
| 开头 | 3句话内有观点，标题就是观点 |
| 结构 | 按逻辑递进，不是并列 |
| 观点 | 每板块有观点输出 |
| 数据 | 有数据引用/表格 |
| 段落 | 每段不超过3行 |
| 字数 | 1500-2500字 |
| 排版 | 对标量子位风格 |

## Step 5: 循环修改

- 第1轮：检查主线、观点、结构
- 第2轮：优化排版、配图、金句
- 最多3轮

## Step 6: 发布到微信公众号

```bash
curl -X POST "https://ai-news-production-2735.up.railway.app/api/publish_wechat" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [{
      "title": "标题",
      "content": "<完整HTML>",
      "digest": "摘要",
      "source_url": "https://example.com"
    }]
  }'
```

## Step 7: 返回结果

告诉用户：
1. 热点新闻
2. 文章标题
3. 字数
4. 评审轮次
5. ✅ 已发布
6. media_id

---

# 去重检查

```bash
cat ~/.openclaw/workspace/published_articles.json
```