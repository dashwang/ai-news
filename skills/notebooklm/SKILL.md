---
name: notebooklm
description: 通过 Google NotebookLM 从 URL 生成 AI 视频/PPT，并自动发布到微信公众号
triggers:
  - 命令: notebooklm ppt <URL>
  - 命令: notebooklm video <URL>
  - 命令: 生成 AI PPT <URL>
  - 命令: 生成 AI 视频 <URL>
  - 命令: 视频生成 <URL>
---

# NotebookLM AI 内容生成技能

通过 Google NotebookLM 将任意 URL (PDF、网站、YouTube) 转化为 AI 生成的视频或 PPT。

## 首次设置

### 1. 安装依赖

```bash
pip install notebooklm-py
```

### 2. 登录 NotebookLM

```bash
notebooklm login
```

这会打开浏览器，请登录你的 Google 账户。登录信息会保存在本地，后续无需重复登录。

## 使用方法

### 触发命令

| 命令 | 说明 |
|------|------|
| `notebooklm ppt <URL>` | 生成 PPT |
| `notebooklm video <URL>` | 生成视频 |
| `生成 AI PPT <URL>` | 生成 PPT |
| `生成 AI 视频 <URL>` | 生成视频 |

### 支持的源类型

- **PDF 文件** - 直接 URL 或本地文件
- **网站 URL** - 文章、博客等
- **YouTube 视频** - 自动提取字幕
- **Google Docs** - 需要可访问权限

## 完整流程

### Step 1: 解析用户输入

用户输入可能是：
- 直接 URL：`https://example.com/article`
- 带命令：`生成 AI PPT https://...`

提取出纯 URL。

### Step 2: 调用 NotebookLM

```python
from notebooklm import NotebookLMClient

# 登录（首次）
client = await NotebookLMClient.from_storage()

# 创建笔记本
notebook = await client.notebooks.create("AI内容")

# 添加源
source = await client.sources.add(notebook, url=url)

# 生成 PPT
slides = await client.slide_deck.create(notebook, language="zh-CN")
slides = await client.slide_deck.wait_for_completion(slides)
await client.slide_deck.download(slides, "output.pptx")

# 生成视频（可选）
video = await client.videos.create(notebook, format="brief", style="whiteboard")
video = await client.videos.wait_for_completion(video)
await client.videos.download(video, "output.mp4")
```

### Step 3: 生成选项

**PPT 选项：**
- 语言：`zh-CN`（中文）

**视频选项：**
- 格式：`brief`（简短）或 `explainer`（详解）
- 风格：`auto_select`, `classic`, `whiteboard`, `anime`, `watercolor`, `kawaii`
- 语言：`zh-CN`

### Step 4: 下载文件

生成的文件保存在：
```
output/notebooklm/
├── notebooklm_slides_20260309_143022.pptx
└── notebooklm_video_20260309_143022.mp4
```

### Step 5: 发布到微信公众号

#### 方案 A：手动发布（推荐）

1. 下载 PPT/视频到本地
2. 登录微信公众号后台
3. 视频 → 草稿箱 → 新建 → 视频上传
4. PPT → 转换为 PDF 或直接提供下载链接

#### 方案 B：嵌入文章

生成图文消息，将视频/PPT 作为附件：

```html
<p style="text-align: center;">
  <strong>📺 AI 视频解读</strong>
</p>
<p style="text-align: center; color: #666;">
  点击下方链接查看完整视频
</p>
<p style="text-align: center;">
  <a href="视频链接">🎬 观看视频</a>
</p>

<p style="text-align: center; margin-top: 20px;">
  <strong>📊 PPT 演示文稿</strong>
</p>
<p style="text-align: center;">
  <a href="PPT下载链接">⬇️ 下载 PPT</a>
</p>
```

## 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `NOTEBOOKLM_OUTPUT_DIR` | 输出目录 | `output/notebooklm` |

### 微信公众号视频限制

- 大小：≤ 20MB（普通公众号）/ ≤ 1GB（视频号）
- 格式：mp4, avi, mov, wmv, flv, mkv
- 时长：≤ 10分钟（普通公众号）

如需上传更大视频，建议：
1. 先上传到视频号
2. 在公众号文章中嵌入视频号链接

## 故障排除

### 登录失败

```bash
# 清除缓存后重新登录
rm -rf ~/.notebooklm-*
notebooklm login
```

### 生成超时

视频生成可能需要 5-30 分钟，可以使用 `--wait` 参数等待完成。

### 源不支持

NotebookLM 支持的源：
- ✅ PDF、网站、YouTube、Google Docs
- ❌ 付费内容、需要登录的页面

## 示例

### 示例 1：生成 AI 播客视频

```
用户：生成 AI 视频 https://www.youtube.com/watch?v=example

系统：
1. 🔗 连接到 NotebookLM...
2. ✅ 添加 YouTube 源
3. 🎬 正在生成视频（可能需要几分钟）...
4. ⏳ 等待生成完成...
5. ✅ 视频已保存到 output/notebooklm/notebooklm_video_xxx.mp4
6. 📤 请手动上传到微信公众号后台
```

### 示例 2：生成 PPT

```
用户：生成 AI PPT https://example.com/research.pdf

系统：
1. 🔗 连接到 NotebookLM...
2. ✅ 添加 PDF 源
3. 🎨 正在生成 PPT...
4. ⏳ 等待生成完成...
5. ✅ PPT 已保存到 output/notebooklm/notebooklm_slides_xxx.pptx
6. 📤 请手动上传到微信公众号后台
```

## 注意事项

1. **生成时间**：PPT 约 1-2 分钟，视频约 5-30 分钟
2. **免费额度**：NotebookLM 免费版有生成次数限制
3. **内容准确性**：AI 生成的内容可能存在偏差，请审核后再发布
4. **版权问题**：确保你有权利使用和发布源内容
