---
name: AI News
description: 一键执行AI新闻完整pipeline：抓取→翻译→发布到公众号
triggers:
  - 命令: AI News
  - 命令: ai news
  - 命令: AI新闻
  - 命令: 发布AI新闻

# Worker 执行顺序
# 1. fetch-news - 抓取新闻
# 2. translate (LLM) - 翻译新闻 (由对话中的LLM自动处理)
# 3. publish-wechat - 发布公众号

# 工作目录
WORKDIR: "~/Projects/llms/agent/ai-news"

---

# AI News Pipeline

## 架构说明
- fetch-news: 独立skill，负责抓取原始新闻
- translate: 由对话中的LLM自动处理（在fetch和publish之间）
- publish-wechat: 独立skill，负责生成HTML并发布

## 执行流程

### Step 1: 抓取新闻 (fetch-news skill)
```bash
cd ~/Projects/llms/agent/ai-news
python3 fetch_worker.py
```
- 从RSS源抓取AI新闻
- 过滤重复内容
- 保存到 news_raw.json
- 输出: 抓取条目数

### Step 2: 翻译新闻 (LLM自动处理)
读取 news_raw.json，调用当前对话的LLM翻译每条新闻的 title 和 summary，生成 news_translated.json

翻译要求：
- 标题翻译：简洁、有信息量
- 摘要翻译：140字+，保留核心信息
- 输出JSON格式，包含 title_zh, summary_zh 字段

### Step 3: 发布公众号 (publish-wechat skill)
```bash
cd ~/Projects/llms/agent/ai-news
python3 publish_worker.py
```
- 读取 news_translated.json
- 检查去重
- 生成公众号HTML
- 发布到草稿箱（或生成HTML预览）
- 更新历史记录

## 完整执行流程

1. 调用 fetch-news skill 抓取新闻
2. 使用当前对话的LLM翻译 news_raw.json → news_translated.json
3. 调用 publish-wechat skill 发布

## 返回结果

告诉用户：
1. 抓取了 X 条新闻
2. 翻译了 Y 条新闻
3. ✅ 已发布到微信公众号草稿箱 / 生成了HTML预览
4. 提醒用户去公众号后台确认发布（如有media_id）

## 检查清单
- [ ] Step 1 成功执行 (fetch_news)
- [ ] Step 2 成功执行 (LLM翻译)
- [ ] Step 3 成功执行 (publish_wechat)
- [ ] 打印完整统计

---

# 排版规范（2026年4月1日最新版）

## 1. 内容精简原则
- 每个新闻模块最多保留 **4条新闻**
- 标题要吸引眼球但不夸张，有信息量
- 摘要100-140字，简洁有力

## 2. 热点聚焦模块（最重要！）
- 选择标准：当日最具话题性的AI新闻
- 白色背景 + 橙色边框（与下方区别开）
- 标题居中 + 橙色高亮
- 内容居中显示

## 3. 模块顺序动态调整（重要！）
- 置顶文章对应的模块也要置顶
- 例如：热点是SubStack的文章 → SubStack模块放到第一个
- 添加【置顶】标记在模块标题后面，如：【置顶】SubStack
- 其他模块按默认顺序：HackerNews → ProductHunt → TechCrunch → SubStack
- **热点文章在其所属模块中也要置顶显示**

## 3. 四平台子标题（每个平台独立颜色）
| 平台 | 文字颜色 | 背景颜色 |
|------|----------|----------|
| HackerNews | #e65100 橙色 | #fff3e0 |
| ProductHunt | #c2185b 粉色 | #fce4ec |
| SubStack | #f57c00 金色 | #fff8e1 |
| TechCrunch | #2e7d32 绿色 | #e8f5e9 |

## 4. 文章标题和摘要格式
- 标题必须是中文，翻译自英文原文
- 标题加粗黑体（使用 `<strong>` 标签）
- 摘要140字+，不要太空
- 摘要用深灰色 #555

## 5. 配图选择规则（重要！）
- 不要随机生成配图
- 根据文章主题选择相关图片：
  - CLI/Terminal主题 → 终端/命令行图片
  - NVIDIA/GPU主题 → 芯片/服务器图片
  - 自动驾驶/Waymo主题 → 汽车/无人车图片
  - AI Agent主题 → 机器人/代码图片

## 6. HTML模板参考

```html
<!-- 热点聚焦模块 -->
<div style="background: #fff; border: 2px solid #e65100; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
    <h2 style="text-align: center; color: #e65100; font-size: 20px; margin-bottom: 15px;">🔥 热点聚焦</h2>
    <p style="text-align: center;"><strong style="color: #1a1a2e; font-size: 18px;">文章标题</strong></p>
    <p style="text-align: center; color: #555; font-size: 14px; line-height: 1.8;">文章摘要...</p>
    <p style="text-align: center; color: #e65100; font-size: 13px; font-style: italic;">💡 点评</p>
</div>

<!-- 分类模块 -->
<h3 style="color: #e65100; font-size: 17px; font-weight: bold; background: #fff3e0; padding: 10px 15px; border-radius: 8px; margin: 25px 0 15px;">🔥 HackerNews</h3>

<!-- 文章块 -->
<div style="margin: 18px 0; padding: 15px; background: #f8f9fa; border-radius: 8px;">
    <p style="margin: 0 0 8px;"><strong style="color: #1a1a2e; font-size: 16px;">文章标题</strong></p>
    <p style="margin: 0 0 10px; color: #555; font-size: 14px; line-height: 1.7;">文章摘要...</p>
    <p style="margin: 0; color: #e65100; font-size: 13px; font-style: italic;">💡 点评</p>
</div>
```
