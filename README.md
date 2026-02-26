# AI News - 每日 AI 科技早报

每日自动抓取全球 AI 科技资讯，翻译、排版，推送到微信公众号。

## 功能

- 🤖 自动抓取 TechCrunch、Hacker News、Product Hunt、SubStack、OpenAI 等源
- 🌐 调用本地 DeepSeek (r1:7b) 自动翻译
- 📱 微信公众号自动发布
- ⏰ 每天 8:00 自动执行

## 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行服务
python app.py
```

## Vercel 部署

```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署
vercel
```

## 环境变量

需要配置以下环境变量：
- `WECHAT_APP_ID` - 微信公众号 AppID
- `WECHAT_APP_SECRET` - 微信公众号 AppSecret
- `TRANSLATION_API_URL` - 翻译服务地址（可选，默认 http://127.0.0.1:5003/translate）
# ai-news
