# KiloClaw Memory

## 自我进化日志

### 2026-05-12 - AI News Publisher Skill 自愈能力增强 & 标点 Bug 修复

**事件 1**: LLM 翻译 API 调用失败导致新闻翻译全是模板文本

**问题诊断**:... [见上文]

**事件 2**: HTML 摘要末尾多出 `...` 省略号

**问题诊断**:
- `build-and-publish-v5.mjs` line 68 模板中 `${s}...` 硬编码了三个点
- 所有 15 条新闻摘要末尾都出现 `...`
- 影响：文章末尾不干净，有冗余标点

**修复过程**:
1. **检测**: 查看 HTML 源码发现每个 `<div>` 摘要块结尾都有 `...`
2. **定位**: 在 `sectionHTML()` 函数的 template string 中找到 `${s}...`
3. **修复**: 改为 `${s}` 移除后缀
4. **验证**: 重新生成 HTML（10,748 字符 vs 之前 10,793），确认无多余点号
5. **发布**: 创建新草稿，Media ID 更新

**skill 改进**:
- ✅ SKILL.md v5.3.1 - Known Issues 章节记录此 bug
- ✅ build-and-publish-v5.mjs 模板移除 `...` 后缀
- ✅ 翻译质量检查增加：扫描摘要是否以 `...` 或空白标点结尾

**关键经验**:
- ❌ HTML 模板字符串中不要硬缀省略号——摘要本身应完整
- ✅ 后处理阶段的质量检查应包括标点残留检测
- ✅ 生成 HTML 后应抽样验证前 3 条摘要的结尾字符

**状态**: ✅ 已修复，v5.3.1 部署

---

## 项目笔记

### AI News Publisher
- 每日自动抓取 5 个源（HN, TechCrunch, LatentSpace, TheDecoder, MIT Tech Review）
- 使用 LLM 翻译为中文
- 生成微信公众号文章草稿
- **新能力**: 即使 LLM 挂掉也能产出可用翻译（7/10 分）

---

### 2026-05-16 - AI News Skill 手动编排成功

**执行方式**: 绕过 `agent-proper.js` 交互式瓶颈，直接分步执行

**步骤 1 — Fetch**: `NEWS_DATE=2026-05-16 node fetch_news.js`
- 5 源各 5 条 = 25 条原始新闻
- TechCrunch AI · Hacker News · Latent Space · The Decoder · MIT Tech Review 全部正常

**步骤 2 — 翻译**: 手动编排 - LLM 生成 Python 脚本 → 写入 `generate-20260516.py` + `generate-20260516.py`
- 遇到 `kilo` 交互式 CLI 不兼容 `execSync | pipe` 的问题 (spawnSync ETIMEDOUT)
- 绕过：直接用 KiloClaw LLM 能力生成翻译 dict 并写入 Python 脚本执行

**翻译遭遇的坑**:
- JSON title key 中的特殊 unicode 字符导致 dict key 不匹配：`\xa0` (NBSP)、`\u2019` (right single quote)、`\u2014` (em-dash)、`\u2013` (en-dash)
- Python 硬编码 `\uXXXX` 转义 key 成功匹配，4 篇修复：TechCrunch×3 (OpenAI trial, Silicon Valley's, Runway) + Substack×1 (Abridge)
- 最终 `Still English-only: NONE ✓`，15/15 全部中文标题

**步骤 3 — HTML 生成**: 978 行 Python inline 脚本 → 8 901 字符 HTML
- 质量检查: 3 section headers, 19 rows, zero `...` 结尾, 0 英文残留标题
- 归档: `wechat-html-2026-05-16.html` + `wechat-html-2026-05-16-{ts}.html`

**头条**: 英国主权大模型推理：AI自主可控的技术路径 (HackerNews, score=104)

**未执行**: `--publish`（未发布到公众号），HTML 已存完毕等待后续推送

**改进点**:
- ❌ `agent-proper.js` standalone fallback 用 `execSync | kilo` 不可行，kilo 是交互式 REPL
- ✅ 完整 pipeline 可外部编排：fetch → translate → generate HTML → publish (逐步骤替代)
- ✅ translate dict 需用 `json.loads` 原生 key 构建，禁止硬编码 ascii 近似 key

---

### 2026-05-18 - 微信公众号 HTML 图片显示修复 & publish-article.mjs v2

**问题**：公众号草稿 `<img>` 标签中只要 src 不是微信 CDN 地址，图片一律不渲染。

**根因**：微信公众号渲染引擎有严格的 URL 白名单，外部链接（GitHub、Unsplash 等）全部被屏蔽。

**修复方法**：
1. 解析 HTML 提取所有 `<img src="https://...">` 中的远程 URL
2. 逐张下载图片 → 调用微信素材库上传 API（`material/add_material?type=image`）
3. 拿到微信 CDN 地址 `mmbiz.qpic.cn/…` → 替换 HTML 中的远程 URL
4. 用替换后的 HTML 创建草稿

**验证**：4 张架构图全部成功替换，草稿正常渲染。

**新关键经验**：
- ❌ **公众号 HTML 禁止引外站图片 src**：必须走微信素材库 → CDN
- ❌ markdown 图片语法 `![alt](url)` 在公众号编辑器无效
- ✅ `<img src="mmbiz.qpic.cn/…">` 是公众号正文插图的唯一可靠方案
- ✅ `publish-article.mjs` 自动完成「远程图 → 下载 → 上传 → CDN → 替换」全流程
- ⚠️ 微信 CDN 图片限制：目前仅测试 png 格式，理论上 jpg/jpeg 也 OK
- ⚠️ `freepublish/submit` 的 `autopublish (48001: api unauthorized)` 是正常现象，手动群发即可
