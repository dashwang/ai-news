---
name: article-translator
description: 根据用户指定的URL，抓取文章内容，翻译成中文，并抓取文中图片作为插图
triggers:
  - 命令: 翻译文章
  - 命令: 翻译这篇
  - 命令: article translate

# 使用方法

当用户给你一个URL并要求翻译成中文时：

1. 使用 `web_fetch` 工具获取文章内容（maxChars设置为15000以上）
2. 提取文章中的图片URL（通常在返回内容的 `https://substackcdn.com/image/fetch/` 或类似图片托管站点）
3. 将文章内容翻译成流畅的中文
4. 将图片嵌入到适当位置作为插图
5. 输出完整的Markdown格式中文文章

# 写作风格要求

- 标题党一点，用emoji吸引读者
- 科技、有温度、懂人性、不浮夸
- 每段140字以上
- 保留文章的核心信息和观点
- 图片用Markdown格式插入：`![描述](图片URL)`

# 输出格式

```markdown
# [翻译后的中文标题]

[开场白段落]

![图片描述](图片URL)

[正文...]

![图片描述](图片URL)

[更多正文和图片...]

---

*原文来源： [原始URL]*
```

# 示例

用户输入：`翻译 https://www.oneusefulthing.org/p/a-guide-to-which-ai-to-use-in-the`

执行：
1. fetch文章内容
2. 提取图片URL
3. 翻译成中文并嵌入图片
4. 输出完整文章
