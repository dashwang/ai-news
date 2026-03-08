# 每日财经 - 自动抓取发布

## 概述

自动抓取当日最热财经新闻，编辑成微信公众号爆款文章格式并发布。

## 数据源（财经平台）

1. **华尔街见闻** - `https://wallstreetcn.com/rss/news`
2. **彭博社 Bloomberg** - `https://feeds.bloomberg.com/markets/news.rss`
3. **36氪** - `https://www.36kr.com/feed/`
4. **虎嗅** - `https://www.huxiu.com/rss`
5. **FT 中文网** - `https://www.ftchinese.com/rss`
6. **新浪财经** - `https://finance.sina.com.cn/rss/index.html`

## 微信公众号排版标准

### 封面区域 - 金色商务风

```html
<!-- 封面：金色商务风 -->
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #D4AF37 0%, #F5D061 100%); border-radius: 0;">
  <span style="font-size: 14px; color: #fff; opacity: 0.9;">📈 发财小萄子</span>
</p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">
  💰 重磅！A股传来大消息
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">
  央行出手，A股迎来重磅利好
</p>
```

### 分区标题样式

```html
<!-- 分区标题 -->
<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #e8f4f8; border-radius: 8px; border-left: 4px solid #1a3a5c;">
  <strong style="font-size: 16px; color: #1a3a5c;">🔥 华尔街见闻</strong>
</p>
```

### 平台颜色主题

| 平台 | 颜色 | emoji |
|------|------|-------|
| 华尔街见闻 | #D4AF37 | 📈 |
| 彭博社 | #000000 | 💼 |
| 36氪 | #FF6900 | 🚀 |
| 虎嗅 | #4A90D9 | 🐅 |
| FT中文网 | #003366 | 🇬🇧 |
| 新浪财经 | #E60012 | 📊 |

### 结尾模板 - 商务稳重风

```html
<!-- 结尾：商务风 + 公众号二维码 -->
<p style="text-align: center; margin-top: 30px; padding: 25px 20px; background: #fafafa; border-radius: 12px; border: 1px solid #eee;">
  <span style="font-size: 16px; color: #333; font-weight: 500;">
    👍 觉得有用？不妨分享给朋友 👏
  </span>
</p>

<!-- 公众号二维码 -->
<p style="text-align: center; margin-top: 20px;">
  <img src="images/qrcode.png" 
       style="width: 120px; height: 120px; border-radius: 8px;" 
       alt="发财小萄子公众号">
</p>
<p style="text-align: center; margin-top: 10px; font-size: 13px; color: #666;">
  📱 扫码关注「发财小萄子」<br>
  每天早上8点自动送达
</p>

<p style="text-align: center; margin-top: 20px; font-size: 13px; color: #999; line-height: 1.6;">
  💬 欢迎评论交流，说说你的看法
</p>
<p style="text-align: center; margin-top: 15px; font-size: 11px; color: #ccc; letter-spacing: 1px;">
  © 2026 发财小萄子 | 认真做内容
</p>
```

## 完整示例

```html
<!-- 封面 -->
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #D4AF37 0%, #F5D061 100%); border-radius: 0;">
  <span style="font-size: 14px; color: #fff; opacity: 0.9;">📈 发财小萄子</span>
</p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">
  💰 重磅！央行降息落地
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">
  A股迎来重磅利好，楼市也有大消息
</p>

<!-- 华尔街见闻 -->
<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff8e8; border-radius: 8px; border-left: 4px solid #D4AF37;">
  <strong style="font-size: 16px; color: #D4AF37;">📈 华尔街见闻</strong>
</p>

<p style="margin: 15px 0 5px 0;">
  <strong style="font-size: 15px; color: #1a1a1a;">1. 央行降息25个基点，释放什么信号？</strong>
</p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">
  央行今日宣布降息25个基点，这是自2024年以来的首次降息操作...
</p>
<p style="margin: 5px 0 15px 0; border-bottom: 1px dashed #eee;"></p>

<!-- 36氪 -->
<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff5ed; border-radius: 8px; border-left: 4px solid #FF6900;">
  <strong style="font-size: 16px; color: #FF6900;">🚀 36氪</strong>
</p>

<!-- 结尾 -->
<p: center; margin-top: 30 style="text-alignpx; padding: 25px 20px; background: #fafafa; border-radius: 12px; border: 1px solid #eee;">
  <span style="font-size: 16px; color: #333; font-weight: 500;">
    👍 觉得有用？不妨分享给朋友 👏
  </span>
</p>

<p style="text-align: center; margin-top: 20px;">
  <img src="images/qrcode.png" 
       style="width: 120px; height: 120px; border-radius: 8px;" 
       alt="发财小萄子公众号">
</p>
<p style="text-align: center; margin-top: 10px; font-size: 13px; color: #666;">
  📱 扫码关注「发财小萄子」<br>
  每天早上8点自动送达
</p>

<p style="text-align: center; margin-top: 20px; font-size: 13px; color: #999; line-height: 1.6;">
  💬 欢迎评论交流，说说你的看法
</p>
<p style="text-align: center; margin-top: 15px; font-size: 11px; color: #ccc; letter-spacing: 1px;">
  © 2026 发财小萄子 | 认真做内容
</p>
```

## 开头模板库（商务吸睛风）

### 模板1：数字吸睛
```html
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #D4AF37 0%, #F5D061 100%); border-radius: 0;">
  <span style="font-size: 14px; color: #fff; opacity: 0.9;">📈 发财小萄子</span>
</p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">
  💰 突发！A股暴涨200点
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">
  央行重磅利好，A股迎来大反弹
</p>
```

### 模板2：悬念吸睛
```html
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #D4AF37 0%, #F5D061 100%); border-radius: 0;">
  <span style="font-size: 14px; color: #fff; opacity: 0.9;">📈 发财小萄子</span>
</p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">
  ❓ 央行罕见动作，释放什么信号？
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">
  市场解读：这次降息不简单
</p>
```

### 模板3：新闻联播风
```html
<p style="text-align: center; margin: 0; padding: 30px 20px; background: linear-gradient(135deg, #D4AF37 0%, #F5D061 100%); border-radius: 0;">
  <span style="font-size: 14px; color: #fff; opacity: 0.9;">📈 发财小萄子</span>
</p>
<p style="text-align: center; font-size: 26px; font-weight: bold; color: #1a1a1a; margin: 20px 15px 10px 15px; line-height: 1.4;">
  🔥 2026.03.08 财经必读
</p>
<p style="text-align: center; color: #666; font-size: 14px; margin: 0 20px 20px 20px;">
  这一天的财经新闻，信息量很大
</p>
```

## 结尾模板库

### 模板1：互动引导 + 公众号二维码
```html
<p style="text-align: center; margin-top: 30px; padding: 25px 20px; background: #fafafa; border-radius: 12px; border: 1px solid #eee;">
  <span style="font-size: 16px; color: #333; font-weight: 500;">
    👍 觉得有用？不妨分享给朋友 👏
  </span>
</p>

<p style="text-align: center; margin-top: 20px;">
  <img src="images/qrcode.png" 
       style="width: 120px; height: 120px; border-radius: 8px;" 
       alt="发财小萄子公众号">
</p>
<p style="text-align: center; margin-top: 10px; font-size: 13px; color: #666;">
  📱 扫码关注「发财小萄子」<br>
  每天早上8点自动送达
</p>
```

### 模板2：关注引导
```html
<p style="text-align: center; margin-top: 30px; padding: 25px 20px; background: #fafafa; border-radius: 12px; border: 1px solid #eee;">
  <span style="font-size: 15px; color: #666;">
    📱 每天8点 | 点关注不迷路<br>
    💬 评论区聊聊，你最关注哪条？
  </span>
</p>
```

## 微信公众号配置

- **公众号名称**: 发财小萄子
- **APP_ID**: wx1b825a0fe3697d04
- **APP_SECRET**: d11e1dfd4c9cc47ca5c095f1df2fd386
- **发布方式**: 直接调用微信 API（非 Railway）
- **发布时检查**: 确认标题包含"发财小萄子"，确认发送到正确公众号

## 微信 API 发布代码

```python
import requests

APP_ID = 'wx1b825a0fe3697d04'
APP_SECRET = 'd11e1dfd4c9cc47ca5c095f1df2fd386'

# 1. 获取 access_token
resp = requests.get(f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}')
token = resp.json()['access_token']

# 2. 创建草稿
article = {
    "title": "标题",
    "content": "HTML内容",
    "digest": "摘要"
}

resp = requests.post(
    f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}',
    json={"articles": [article]}
)
print(resp.json())
```

## 常见问题

1. **Railway 500 错误** - 检查 RSS 源是否有效
2. **微信 IP 白名单** - 需要在微信开放平台添加 Railway 服务器 IP
3. **新闻不足** - 需要检查各 RSS 源是否正常返回数据

## 后续迭代方向

- [ ] 增加更多财经新闻源（雪球、同花顺）
- [ ] A股、港股、美股分板块整理
- [ ] 个性化推荐（根据用户兴趣）
- [ ] 多平台发布（公众号、雪球）
- [ ] 趋势分析图表
- [ ] A/B测试不同开头/结尾效果
