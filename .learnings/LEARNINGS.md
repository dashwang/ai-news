# 学习记录

## [LRN-20260312-001] correction

**Logged**: 2026-03-12T01:28:00Z
**Priority**: high
**Status**: resolved
**Area**: workflow

### Summary
微信公众号推送时内容为空

### Details
在发送JSON到微信公众号时，使用了错误的shell语法：
```bash
"content": "$(cat /tmp/ai_news_0312.html)"
```
单引号内的 $(...) 不会被执行，而是被当作 literal string 发送。导致实际发送的内容只有 392 字节（几乎是空的）。

### Suggested Action
使用Python直接读取文件并构建JSON，而不是用shell字符串插值：
```python
with open('/tmp/ai_news_0312.html', 'r') as f:
    html_content = f.read()
payload = {"articles": [{"content": html_content}]}
```

### Metadata
- Source: user_feedback
- Related Files: /tmp/ai_news_0312_v2.html

---

## [LRN-20260312-002] correction

**Logged**: 2026-03-12T01:22:00Z
**Priority**: high
**Status**: resolved
**Area**: workflow

### Summary
AI News 每个平台文章数量不足

### Details
用户要求每个子模块至少4-5篇文章，但我第一次只抓取了1-2篇。没有仔细阅读skill中的格式要求就匆匆发布。

### Suggested Action
发布前严格按照skill中的格式检查清单验证：
- [ ] 每平台4-5篇
- [ ] 每条新闻140字+
- [ ] 4平台用不同颜色边框背景
- [ ] 去重检查

### Metadata
- Source: user_feedback

---

## [LRN-20260312-003] knowledge_gap

**Logged**: 2026-03-12T04:05:00Z
**Priority**: low
**Status**: resolved
**Area**: workflow

### Summary
BOOTSTRAP.md 存在但没有按照指示执行

### Details
打开workspace时，AGENTS.md 中提到如果 BOOTSTRAP.md 存在应该按照它来执行。但我每次都直接读取现有文件，没有检查是否有这个初始化文件。

### Suggested Action
每次打开新workspace时，检查 BOOTSTREP.md 是否存在，如果存在则按照指示执行初始化流程。

### Metadata
- Source: conversation

---

## [LRN-20260312-004] correction

**Logged**: 2026-03-12T04:06:00Z
**Priority**: medium
**Status**: resolved
**Area**: workflow

### Summary
首次响应不够详细，没有使用skill

### Details
用户首次说"AI news"时，我只是简单汇总了搜索结果，没有：1) 检查是否有自定义skill 2) 严格按照skill格式 3) 发布到微信公众号

### Metadata
- Source: conversation

---

## [LRN-20260312-005] auto_evolution

**Logged**: 2026-03-12T12:20:00Z
**Priority**: medium
**Status**: resolved
**Area**: workflow

### Summary
实现自动进化：热内容置顶功能

### Details
按照用户要求更新了skill，增加了"热标题内容置顶"功能：
1. 动态标题对应的内容放在全文第一篇（开场白之后）
2. 新增"热点聚焦"板块
3. 人类学习方法：最重要的内容最先看到

### Metadata
- Source: user_instruction
- Related: fetch-ai-news/SKILL.md

---
