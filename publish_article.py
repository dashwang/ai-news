#!/usr/bin/env python3
import requests
import json
import re
import os

WECHAT_APP_ID = "wxa87b65ba78d3c822"
WECHAT_APP_SECRET = "ac6a029c2b4ef7c1b89fbaeeaace3931"

# 获取token
resp = requests.get(f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}")
token = resp.json()["access_token"]
print(f"Token: {token[:20]}...")

# 读取文章内容
with open("/root/.openclaw/workspace/zhipu-ai-zhangpeng-article.md", "r") as f:
    original_content = f.read()

# 解析文章内容 - 提取标题和正文
lines = original_content.strip().split("\n")
title = ""
content_start = 0

for i, line in enumerate(lines):
    if line.startswith("# "):
        title = line.replace("# ", "").strip()
        content_start = i + 1
        break

# 获取正文部分
body = "\n".join(lines[content_start:])

# 转换为HTML格式（公众号需要）
# 1. 将markdown标题转换为HTML
html_body = body
html_body = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_body, flags=re.MULTILINE)
html_body = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_body, flags=re.MULTILINE)

# 2. 将段落用p标签包裹
lines = html_body.split("\n\n")
html_paragraphs = []
for para in lines:
    if para.strip():
        if para.startswith("<h") or para.startswith("<p"):
            html_paragraphs.append(para)
        else:
            html_paragraphs.append(f"<p>{para.strip()}</p>")

final_html = "".join(html_paragraphs)

# 添加公众号底部信息
footer = """
<p style="text-align: center; color: #888; font-size: 12px; margin-top: 30px;">
---<br>
扫码关注我们<br>
<img src="http://mmbiz.qpic.cn/sz_mmbiz_jpg/Rv7jxicObXS2mndXVWe53l5Gk4pebyX1icYCa2RZnWKCtRk8V5Q0EwpKtHhjp7RlRMNAJXpPYezMNZWibWJYyDXkcUsfZHJicat9Sx0O3KHWrFM/0?wx_fmt=jpeg" width="180">
</p>
"""

# 创建图文素材
article = {
    "title": title,
    "author": "小龙虾",
    "content": final_html + footer,
    "content_source_url": "https://www.zhipuai.cn",
    "digest": "深度讲述智谱AI CEO张鹏的创业故事和技术理想",
    "thumb_media_id": "rU9uuMjCA4SOhGtWuHLjGs4TULM5a2hbiRAvuE2ONNpa6_BkjSCpIMJIqZDrr7B-",
    "need_open_comment": 0,
    "can_comment": 0
}

# 调用创建草稿接口
url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
resp = requests.post(url, json=article)
result = resp.json()

print("创建结果:", json.dumps(result, ensure_ascii=False, indent=2))
