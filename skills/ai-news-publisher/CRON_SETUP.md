# AI News Publisher - 定时任务设置

## 概述
每天早上7点（Asia/Shanghai 时区）自动抓取、翻译并发布AI新闻到微信公众号草稿箱。

## 组件
- **Script**: `/root/.openclaw/workspace/skills/ai-news-publisher/daily-run.sh`
- **Skill**: `ai-news-publisher` (v5.3.1)
- **Cron**: `/etc/cron.d/ai-news-publisher` (UTC 23:00 = Asia/Shanghai 07:00)

## 工作流程
1. **Fetch** (`fetch_news.js`): 从5个源抓取当天AI新闻，生成 `news-YYYY-MM-DD.json`
2. **Translate** (`agent-proper.js`): 使用 KiloClaw LLM 翻译标题和摘要，生成HTML
3. **Publish** (`agent.js --publish`): 上传HTML和封面图到微信公众号草稿箱

## 时区说明
- 系统 cron 使用 UTC 时间：`0 23 * * *` (UTC 23:00)
- 脚本内 `export TZ=Asia/Shanghai`，使用上海时间计算日期
- UTC 23:00 对应 Asia/Shanghai 次日 07:00（早上下班时间）
- fetch_news.js 通过 `NEWS_DATE` 环境变量接收上海日期

## 验证方法

### 干跑测试
```bash
bash /root/.openclaw/workspace/skills/ai-news-publisher/daily-run.sh --dry-run
```

### 完整运行（会发布草稿）
```bash
bash /root/.openclaw/workspace/skills/ai-news-publisher/daily-run.sh
```

### 查看日志
```bash
tail -f /root/.openclaw/workspace/skills/ai-news-publisher/data/cron-$(date +%Y-%m-%d).log
```

### 查看已发布记录
```bash
cat /root/.openclaw/workspace/skills/ai-news-publisher/data/published.json
```

## 检查cron状态
```bash
service cron status
cat /etc/cron.d/ai-news-publisher
```

## 注意事项
- 需要 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET` 环境变量（已在 `.env` 中配置）
- KiloClaw LLM 偶尔可能超时（`ETIMEDOUT`），失败时会使用简单翻译
- 微信公众号草稿箱限制：标题 ≤ 32 字，内容 ≤ 64KB
- 定时任务每天只在 UTC 23:00 触发一次

## 故障排除
如果当天没有发布，检查：
1. cron 服务是否运行: `service cron status`
2. 日志文件是否有错误
3. 环境变量是否正确: `env | grep WECHAT`
4. 微信公众号权限是否正常

## 手动触发
```bash
bash /root/.openclaw/workspace/skills/ai-news-publisher/daily-run.sh
```

---

Created: 2026-05-12
Version: 1.0
