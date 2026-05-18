---
name: ai-news-publisher
description: AI News Publisher - fetch top stories, translate using LLM, publish to WeChat with compact layout, QR code, and deduplication
version: 5.3.1
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
    qrCodeUrl: env:WECHAT_QR_CODE_URL # Optional: auto-inject QR code in footer

---

# AI News Publisher (Agent Skill)

## Usage
```bash
# Run via OpenClaw agent (uses KiloClaw's LLM for translation)
openclaw agent run ai-news-publisher

# With publishing to WeChat draft
openclaw agent run ai-news-publisher --publish

# Custom limit and date
openclaw agent run ai-news-publisher --limit=10 --date=2026-05-02
```

## Features
- ✅ **Smart Section Order**: TechCrunch first (priority), then Hacker News, then Substack (aggregated)
- ✅ **Substack Consolidation**: Latent Space + The Decoder + MIT Tech Review → single "Substack" section
- ✅ **Deduplication**: Automatically removes title repetition in summaries
- ✅ **Compact Layout**: Tighter spacing (8px margins, 6px item padding) for mobile reading
- ✅ **~200-char Summaries**: Expanded summaries with context
- ✅ **Auto QR Code**: Footer includes WeChat QR code (configurable via WECHAT_QR_CODE_URL)
- ✅ **Duplicate Prevention**: Tracks published dates in data/published.json

## Known Issues
- **Trailing ellipsis in summaries** (before v5.3.1): HTML templates added `...` after every summary. Fixed by removing the ellipsis suffix from `build-and-publish-v5.mjs` template. Always verify generated HTML has clean summary endings.
- **Incomplete dictionary coverage**: When `translate.js` dictionary lacks a title, fallback uses raw English. Solution: Ensure dictionary covers all expected news titles for the day before running build.
- **WeChat article body images not rendering** (fixed 2026-05-18): The WeChat draft renderer silently drops any `<img src>` that does not point to a WeChat CDN URL (`mmbiz.qpic.cn`). Externally-hosted images (GitHub, Unsplash, etc.) are stripped at render time and show as blank. **Fix**: `publish-article.mjs` v2 auto-uploads every body image to the WeChat material library (`/cgi-bin/material/add_material?type=image`) and replaces the `src` with the returned CDN URL before creating the draft.

## How it works
1. Fetches news from 5 sources (HN, TechCrunch, LatentSpace, TheDecoder, MIT Tech Review)
2. Sorts by score and takes top N (default 15)
3. **Translates titles & summaries using KiloClaw's built-in LLM** (via agent.llm)
4. **Deduplicates** summaries (removes title repetition)
5. **Expands summaries** to ~200 characters
6. **Generates compact HTML** with TechCrunch section first
7. **Injects QR code** in footer (if WECHAT_QR_CODE_URL is set)
8. Optionally **publishes to WeChat draft box

## Files
- `agent-native.js` - Standalone version (direct node execution)
- `agent-proper.js` - OpenClaw Agent version (uses agent.llm)
- `publish-article.mjs` - WeChat publish helper
- `data/` - Output directory (news JSON, HTML)
- `.env` - Environment config (WECHAT_APP_ID, WECHAT_APP_SECRET, WECHAT_QR_CODE_URL)

## Configuration

### WeChat (Required for Publishing)
```bash
WECHAT_APP_ID=wxaxxxxx
WECHAT_APP_SECRET=your-secret
```

### QR Code (Optional)
```bash
# Your official WeChat QR code URL (downloaded from mp.weixin.qq.com)
WECHAT_QR_CODE_URL=https://mmbiz.qlogo.cn/mmbiz/xxx/0?wx_fmt=png
```

Without QR code, the footer will show a placeholder image.

## Version History
- **5.3.2** (2026-05-18): `publish-article.mjs` v2 — body images are auto-uploaded to WeChat CDN before draft creation; fixed invisible body images bug
- **5.3.0** (2026-05-xx): Stable release with 5-source aggregation, dictionary-based translation, compact WeChat layout
- **5.2.x**: Experimental LLM translation with auto-fallback (rolled back)
- **5.1.x**: Early single-source versions

