# 长期记忆

## 错误与修正

### 1. 微信公众号推送内容为空 (2026-03-12)
**问题**: 使用 `$(cat file)` 在单引号字符串中，不会执行，而是发送 literal string
**解决**: 用Python读取文件并构建JSON
**教训**: Shell字符串插值不适用于JSON payload

### 2. 没有先使用自定义Skill (2026-03-12)
**问题**: 用户要求"AI news"时，直接web搜索，没有先检查是否有对应skill
**解决**: 先读取workspace/skills/下的SKILL.md
**教训**: 用户自定义的skill是处理特定任务的标准方式

### 3. 文章数量不足 (2026-03-12)
**问题**: 每个平台只放了1-2篇，用户要求4-5篇
**解决**: 严格按照skill格式检查清单验证
**教训**: 发布前必须逐项检查

---

## 用户偏好

- AI News: 每平台4-5篇文章
- 格式: 微信公众号HTML格式
- 动态标题+开场白

### 4. 首次响应不够详细 (2026-03-12)
**问题**: 用户首次说"AI news"时，只给了简短汇总，没有用skill
**教训**: 用户要求"X news"类任务时，应该先检查是否有对应skill

### 5. 读取文件路径错误 (2026-03-12)
**问题**: 尝试读取transcript时路径错误
**教训**: OpenClaw的transcript在 /root/.openclaw/agents/main/sessions/ 而不是workspace目录

### 6. 热内容置顶功能 (2026-03-12)
- 动态标题对应内容放全文第一篇
- 新增"热点聚焦"板块
- 模仿人类阅读习惯：最重要内容最先看到

### 自动进化 (2026-03-12)
- 每次被纠正后自动记录到 .learnings/
- 定期推送到 GitHub feature/learnings 分支

### 7. 公众号名称错误 (2026-03-12)
- 问题：底部写的是"AI大航海"而不是"grepAI"
- 解决：在skill中添加"公众号名称：grepAI"检查项
- 教训：生成前必须核对skill中的配置

## TrustMRR深度文章 Skill
- 位置: skills/trustmrr-deep-dive/
- 功能: 抓取TrustMRR排行榜产品，写2000-3000字深度创始人故事
- 触发词: "TrustMRR深度"、"创始人故事"、"产品背后的故事"
- 已使用: 2026-03-12 写了Stan(年入354万美元，增长983%)的创始人Marc Lou故事

## 已创建的所有Skills
1. fetch-ai-news - AI新闻抓取发布
2. trustmrr-deep-dive - TrustMRR深度文章
3. notebooklm-prompts - 幻灯片提示词
4. tiangong-notebooklm-cli - NotebookLM CLI
5. self-improving-agent - 自我进化记录
6. skill-vetter - 安全审查
