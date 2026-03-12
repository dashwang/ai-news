# 错误记录

## [ERR-20260312-001] fetch-ai-news skill

**Logged**: 2026-03-12T01:12:00Z
**Priority**: high
**Status**: resolved
**Area**: workflow

### Summary
没有使用用户自定义的 AI News skill

### Error
用户创建了名为 "fetch-ai-news" 的自定义skill，但我没有先读取skill文档，而是直接用web搜索来回答 "AI news"。

### Context
用户要求 "AI news"，我应该：
1. 先检查是否有相关的自定义skill
2. 读取SKILL.md了解具体流程
3. 按照skill定义的流程执行

### Suggested Fix
在处理用户请求前，先检查workspace/skills/目录是否有对应的skill。

### Resolution
- **Resolved**: 2026-03-12T01:12:00Z
- **Notes**: 后续正确使用了fetch-ai-news skill

---

## [ERR-20260312-002] 会话历史读取失败

**Logged**: 2026-03-12T04:04:00Z
**Priority**: medium
**Status**: resolved
**Area**: workflow

### Summary
无法读取会话历史来检查错误

### Error
用户让我检查历史对话中的错误，但我尝试用 sessions_history 工具时忘记传 sessionKey 参数，导致验证失败。后来找 transcript 文件时路径也不对。

### Context
- 第一次：sessions_history 没传 sessionKey
- 第二次：read 路径错误 /root/.openclaw/workspace/xxx.jsonl
- 正确路径：/root/.openclaw/agents/main/sessions/xxx.jsonl

### Resolution
- **Resolved**: 2026-03-12T04:04:00Z
- **Notes**: 通过 ls 命令找到正确路径后成功读取

---
