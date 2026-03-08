# OpenClaw 爆款文章 - 技能说明

## 概述

生成高质量微信公众号爆款文章，参考量子位/机器之心风格。

## 文章模板

参考 `/root/.openclaw/workspace/skills/ai-news-publisher/openclaw-viral-v7.html`

## 格式规范（量子位/机器之心风格）

### 封面
- 简洁黑色背景
- 白色标题
- 副标题说明用途

### 正文
- 字号：15-16px（紧凑）
- 行距：1.7-1.8
- 段落间距：统一 15-20px
- 去掉花哨装饰

### 颜色方案
- 主标题：#000 黑色背景 + #fff 白色文字
- 重点强调：加粗
- 灰色背景块：#f5f5f5
- 强调边框：4px solid #333

## 字数要求

- 汉字必须超过 **3000 字**
- 统计方法：`grep -o '[\u4e00-\u9fff]' article.html | wc -l`

## 发布

使用 Railway 服务发布到公众号：

```bash
curl -X POST "https://ai-news-production-2735.up.railway.app/api/publish_wechat" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [{
      "title": "标题",
      "content": "HTML内容",
      "digest": "摘要",
      "source_url": "https://docs.openclaw.ai"
    }]
  }'
```

## 素材来源

- OpenClaw 官方文档：docs.openclaw.ai
- GitHub: github.com/openclaw/openclaw
- Discord 社区：discord.gg/clawd
- ClawHub 技能商店：clawhub.com
- Showcase 案例

## 常用模板

### 15 个骚操作案例框架

1. 微信 AI 助手
2. WhatsApp / Telegram 多通道
3. GitHub PR 自动审查
4. 酒窖管理 Skill
5. 语音 + 视觉 AI
6. 自托管隐私
7. 多代理路由
8. Canvas 实时协作
9. 54+ Skills
10. 智能家居
11. 自动写公众号
12. 语音点歌
13. 密码管理
14. 天气查询
15. 自定义技能

### 快速开始

1. 安装：`npm install -g openclaw@latest`
2. 初始化：`openclaw onboard --install-daemon`
3. 启动：`openclaw gateway --port 18789`

## 后续迭代

- [ ] 增加更多案例
- [ ] 优化 SEO 标题
- [ ] 添加互动引导
