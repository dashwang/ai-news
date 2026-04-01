---
name: translate-news
description: 读取news_raw.json，使用LLM翻译成中文，输出到news_translated.json
triggers:
  - 命令: translate news
  - 命令: 翻译AI新闻

# 输入输出
INPUT_FILE: "news_raw.json"
OUTPUT_FILE: "news_translated.json"

# LLM 配置
LLM_MODEL: "claude-sonnet-4-20250514"
LLM_PROVIDER: "anthropic"

---

# Translate News Worker

## 功能
1. 读取 news_raw.json
2. 使用自身 LLM 翻译标题和摘要
3. 保存到 news_translated.json

## 执行命令

```bash
cd ~/.openclaw/workspace/ai-news-backend

python3 translate_worker.py
```

## LLM Prompt 模板

```
请将以下AI新闻标题和摘要翻译成中文，保持专业但有温度的风格。返回一个JSON格式的结果：

标题: {title}
摘要: {summary}

返回格式:
{"title_zh": "...", "summary_zh": "..."}
```

## 输出格式
```json
[
  {
    "id": "uuid",
    "source": "HackerNews",
    "title": "原始标题",
    "title_zh": "翻译后的标题",
    "url": "...",
    "summary": "原始摘要",
    "summary_zh": "翻译后的摘要",
    "timestamp": "ISO8601",
    "translated_at": "ISO8601"
  }
]
```

## 检查清单
- [ ] 读取 news_raw.json 成功
- [ ] 调用 LLM 翻译每条新闻
- [ ] 保存到 news_translated.json
- [ ] 打印翻译统计