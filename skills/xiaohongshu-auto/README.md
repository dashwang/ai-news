# 小红书自动化发布

## 简介

使用 Playwright 实现小红书自动化发布。

## 安装

```bash
npm install
npx playwright install chromium
```

## 使用

```bash
# 默认内容
node xiaohongshu-publish.js

# 自定义内容
node xiaohongshu-publish.js --title "你的标题" --content "你的内容"

# 带图片
node xiaohongshu-publish.js --content "内容" --image "./image.jpg"
```

## 流程

1. 第一次运行需要扫码登录
2. 登录后 cookies 会保存到文件
3. 后续运行会自动使用 cookies
4. 内容填入后等待手动确认发布

## OpenClaw 集成

可以在 OpenClaw 中使用 exec tool 调用：

```
openclaw exec -- node xiaohongshu-publish.js --content "内容"
```

## 注意事项

- 需要保持登录态（cookies 有效期）
- 建议不要频繁自动化操作
- 小红书可能有反爬机制
