# AI News - Daily AI Tech Briefing

Automatically fetch global AI tech news daily, translate, format, and push to WeChat official account.

## Features

- 🤖 Automatically fetch sources from TechCrunch, Hacker News, Product Hunt, SubStack, OpenAI, etc.
- 🌐 Call local DeepSeek (r1:7b) for automatic translation
- 📱 Automatically publish to WeChat official account
- ⏰ Automatically execute at 8:00 AM daily

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run service
python app.py
```

## Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## Railpack Deployment

```bash
# Install Railpack CLI
npm i -g @railpack/cli

# Deploy
railpack deploy
```

## Environment Variables

Configure the following environment variables:
- `WECHAT_APP_ID` - WeChat official account AppID
- `WECHAT_APP_SECRET` - WeChat official account AppSecret
- `TRANSLATION_API_URL` - Translation service URL (optional, default http://127.0.0.1:5003/translate)

# AI News
# AI News
# AI News
# ai-news
# ai-news
