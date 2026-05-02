---
name: ai-news-publisher
description: AI News Publisher - fetch top 15 stories, translate using KiloClaw's LLM, publish to WeChat
version: 6.0.0
author: KiloClaw
license: MIT
homepage: https://github.com/dashwang/ai-news

# OpenClaw Agent Skill
agent:
  entry: agent.js
  capabilities:
    - llm.chat
    - http.get
    - fs.read
    - fs.write
    - child_process.exec

# OpenClaw CLI command
commands:
  - name: run
    description: Fetch AI news, translate with KiloClaw LLM, publish to WeChat draft
    usage: openclaw agent run ai-news-publisher [--publish] [--limit=15]
    agent: ai-news-publisher

# Configuration
config:
  limit: 15
  wechat:
    appId: env:WECHAT_APP_ID
    appSecret: env:WECHAT_APP_SECRET

---

# AI News Publisher (Agent Skill)

## Usage
```bash
# Run via OpenClaw agent (uses KiloClaw's LLM for translation)
openclaw agent run ai-news-publisher

# With publishing
openclaw agent run ai-news-publisher --publish

# Custom limit
openclaw agent run ai-news-publisher --limit=10
```

## How it works
1. Fetches news from 5 sources (HN, TechCrunch, LatentSpace, TheDecoder, MIT Tech Review)
2. Sorts by score and takes top N (default 15)
3. **Translates titles & summaries using KiloClaw's built-in LLM** (via agent.llm)
4. Generates clean HTML (no URLs, summary ≤140 chars)
5. Optionally publishes to WeChat draft box

## Files
- `agent.js` - Main agent logic
- `data/` - Output directory (news JSON, HTML)
- `publish-article.mjs` - WeChat publish helper
