---
name: fetch-ai-news
description: 抓取北美AI新闻，翻译成中文，编排后先写入飞书文档，再发布到微信公众号草稿箱
triggers:
  - 命令: fetch news
  - 命令: 抓取AI新闻
  - 命令: 发布AI新闻
  - 命令: AI News

# Checkpoint 记录

## ✅ 2026.02.28 成功发布
- 格式验证通过：橙色头部 + 4平台彩色边框背景
- 每条新闻140字+ 验证通过
- 微信公众号发布成功
- media_id: rU9uuMjCA4SOhGtWuHLjGj1i4MSoqE5Td_vZRvOIhYnEGGh3kaIvN4M_-3NGyP5T
- 用户确认：这就是我想要的

## ✅ 2026.02.28 晚间特辑发布成功
- 新标题风格：结合热点新闻（"突发！Sam Altman宣布五角大楼交易..."）
- 橙色头部无emoji
- 动态标题：早报/午报/晚报
- 4平台彩色边框居中
- 每条140字+
- 二维码嵌入成功
- 格式检查清单完整

## ✅ 2026.03.02 更新
- 新增去重功能：比对历史发布记录，避免重复
- 新增动态标题：每次根据热点新闻生成吸引眼球的标题
- 新增开场白变化：不同角度切入，避免千篇一律

## 关键要点（已固化到模板）
1. 每条新闻必须140字+
2. 4平台用不同颜色边框背景（不是纯色背景）
3. 正文黑体（color: #333)
4. 标题党一点，用 emoji
5. 不要URL
6. 写作风格：科技、有温度、懂人性、不浮夸
7. 🔥 只在Hacker News标题用一次
8. 橙色头部标题无emoji
9. 二维码URL: https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png
10. **去重：必须比对历史发布，避免重复**
11. **动态标题：每次根据当日热点生成**

## 格式检查清单（每次发布前必检）

### 1. 橙色头部
- [ ] 无emoji（如📰、🔥）
- [ ] 格式：`<p style="...background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%)...>`
- [ ] 动态标题：早报/午报/晚报（根据北京时间）
- [ ] **动态标题内容：根据当日最热的1-2条新闻生成**

### 2. 开场白
- [ ] 有科技感、有温度、不浮夸
- [ ] 引导阅读下文
- [ ] 不使用"炸裂！"等夸张词汇
- [ ] **每次角度不同，不要重复**

### 3. 4个平台标题
- [ ] 居中展示（text-align: center）
- [ ] 🔥 只在Hacker News出现一次
- [ ] 颜色正确：Hacker News #ff6600, Product Hunt #da552f, TechCrunch #0a9900, SubStack #ff4400

### 4. 新闻条目
- [ ] 每条140字+
- [ ] 正文黑体（color: #333）
- [ ] 无URL
- [ ] 标题加粗（color: #1a1a1a）
- [ ] **去重：检查是否已在之前发布过**

### 5. 结尾
- [ ] 二维码URL正确（https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png）
- [ ] 二维码尺寸 180px × 180px
- [ ] 有引导语（"扫码关注"）
- [ ] 有版权信息
---

# AI News 完整流程

当用户要求抓取并发布AI新闻时，执行以下完整流程：

## 飞书文档配置

- **Doc Token**: `XMSudBIsUoGD20x7WKLctFCend9`
- 文档标题：「北美AI News」
- **历史发布记录文件**: `published_articles.json`

## Step 1: 调用 Railway 获取英文新闻

```bash
curl "https://ai-news-production-2735.up.railway.app/api/fetch"
```

返回格式（4个站点）：
```json
{
  "date": "2026-02-28",
  "news": {
    "HackerNews": [],
    "ProductHunt": [],
    "TechCrunch": [],
    "SubStack": []
  },
  "status": "ok"
}
```

## Step 2: 去重检查（重要！）

**必须执行！**
1. 读取历史发布记录：`published_articles.json`
2. 对每条新闻进行比对：
   - 标题相似度 > 80% → 跳过
   - URL相同 → 跳过
3. 只保留**未发布过**的新闻
4. 更新历史记录

**历史记录格式：**
```json
{
  "published": [
    {"title": "...", "url": "...", "date": "2026-03-02"},
    {"title": "...", "url": "...", "date": "2026-03-02"}
  ]
}
```

## Step 3: 动态标题生成（重要！）

**根据当日最热的新闻生成标题，不要千篇一律！**

### 标题生成策略：
1. **找热点**：从SubStack/TechCrunch找出最劲爆的新闻
2. **造句式**：
   - 数字法："$1100亿！XXX创纪录"
   - 疑问法："XXX真的来了？"
   - 对比法："XXX vs XXX"
   - 感叹法："XXX炸锅了"
3. **每天不同**：
   - Day1: "炸裂！XXX"
   - Day2: "突发！XXX"
   - Day3: "重磅！XXX"
   - Day4: "刚刚，XXX"
   - Day5: "XXX火上浇油"

### 示例（2026.03.02）：
- 热点：OpenAI $1100亿融资
- 标题：「$1100亿！OpenAI史诗级融资，AI进入\"核战争\"时代」
- 或：「刚刚！OpenAI刷新史上最大融资纪录」

### 开场白变化：
```python
# 每天用不同的开场角度
openings = [
    "今天的AI圈依然热闹。",           # Day1
    "AI圈又出大新闻。",               # Day2
    "平静的AI圈下，暗流涌动。",       # Day3
    "今天的科技圈，有大事发生。",     # Day4
    "AI行业迎来关键时刻。",           # Day5
]
```

## Step 4: 翻译并编辑

每条新闻需要展开 **140字以上**的中文介绍。

**每条新闻的标题要二次加工：**
- 原文：Motorola announces a partnership with GrapheneOS Foundation
- 加工：Motorola联手GrapheneOS：隐私手机要变天？
- 原则：保留核心信息 + 增加悬念/话题性

## Step 5: 微信公众号排版（重要！）

### 开头模板（动态标题）

```html
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%); border-radius: 0;">
  <span style="font-size: 20px; color: #fff; font-weight: bold;">[动态标题]</span>
</p>

<p style="margin: 25px 20px 20px; font-size: 15px; line-height: 1.8; color: #333; text-align: justify;">
  [动态开场白]
</p>
```

### 4大部分样式
```html
<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff6600; text-align: center;">
  <strong style="font-size: 16px; color: #ff6600;">🔥 Hacker News 热门</strong>
</p>
```

### 新闻条目格式
```html
<p style="margin: 15px 0 5px 0;">
  <strong style="font-size: 15px; color: #1a1a1a;">1. [加工后的标题]</strong>
</p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">
  140字以上的中文展开介绍...
</p>
```

## Step 6: 写入飞书文档

```json
{
  "action": "update_block",
  "doc_token": "XMSudBIsUoGD20x7WKLctFCend9",
  "block_id": "BnJjdiIProug5Lx8vJKc2M9YnTh",
  "content": "完整Markdown内容..."
}
```

## Step 7: 发布到微信公众号草稿箱

```bash
curl -X POST "https://ai-news-production-2735.up.railway.app/api/publish_wechat" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [{
      "title": "[动态标题]",
      "content": "<完整HTML内容>",
      "digest": "今日精选全球AI科技资讯",
      "source_url": "https://veray.ai"
    }]
  }'
```

## Step 8: 更新历史记录

发布成功后，更新 `published_articles.json`：
```json
{
  "published": [
    {"title": "Motorola联手GrapheneOS", "url": "https://...", "date": "2026-03-02"},
    ...
  ]
}
```

## 返回结果

告诉用户：
1. 成功抓取了 X 条新闻（去重后）
2. 已过滤掉 Y 条重复新闻
3. 动态标题：[实际标题]
4. ✅ 已写入飞书文档
5. ✅ 已发布到微信公众号草稿箱
6. 提醒用户去公众号后台确认发布
