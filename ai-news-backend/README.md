# AI News Project

Automated AI news collection and publishing system.

## Features

- **RSS News Fetching**: TechCrunch, HackerNews, ProductHunt, SubStack newsletters
- **Twitter/X Scraper**: Monitor AI influencers and collect tweets
- **Railway Deployment**: Automated daily cron job
- **Multi-platform Publishing**: WeChat, Feishu, etc.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file:

```bash
# Railway specific
DATABASE_URL=sqlite:///data/news.db

# Enable Twitter fetching (optional, requires more resources)
FETCH_TWITTER=true

# Twitter API (optional, for higher rate limits)
# TWITTER_BEARER_TOKEN=your_bearer_token
```

### 3. Run Locally

```bash
# Fetch news
python fetch_news.py

# Or with specific date
python fetch_news.py --date 2026-03-02
```

### 4. Deploy to Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

The Railway configuration in `railway.json` will:
- Build with Python 3.11
- Run cron job daily at 8:00 UTC
- Store data in SQLite database

## Twitter Scraper

### Lightweight Version (Default)

Uses free APIs (fxtwitter, nitter) - no authentication needed:

```python
from twitter_scraper import fetch_twitter_ai_news

tweets = fetch_twitter_ai_news()
```

### Playwright Version (Heavy)

For more reliable scraping, use Playwright:

```bash
pip install playwright
playwright install chromium
```

Then set `USE_PLAYWRIGHT=true` in environment.

## Project Structure

```
.
├── fetch_news.py       # Main news fetcher (RSS)
├── twitter_scraper.py  # Twitter/X scraper
├── app.py              # Flask web server
├── config.json         # Configuration
├── railway.json        # Railway deployment config
├── requirements.txt    # Python dependencies
└── ai-news/            # AI News skill module
    ├── twitter_scraper.py
    └── publish_wechat.py
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite database path | `data/news.db` |
| `FETCH_TWITTER` | Enable Twitter scraping | `false` |
| `PORT` | Server port | `8000` |
| `TWITTER_BEARER_TOKEN` | Twitter API token | - |

## Cron Schedule

Default: `0 8 * * *` (Daily at 8:00 UTC)

Modify in `railway.json` to change.
