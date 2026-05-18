#!/usr/bin/env python3
import requests
import json
import os

app_id = os.environ.get("WECHAT_APP_ID", "wxa87b65ba78d3c822")
app_secret = os.environ.get("WECHAT_APP_SECRET", "ac6a029c2b4ef7c1b89fbaeeaace3931")

resp = requests.get(f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}")
token = resp.json()["access_token"]
print("Token:", token[:20])

with open("/root/.openclaw/workspace/wechat_article_formatted.html", "r", encoding="utf-8") as f:
    content = f.read()

article = {
    "articles": [{
        "title": "智谱AI张鹏：从清华实验室走出的AI探路者",
        "content": content
    }]
}

url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
resp = requests.post(url, json=article)
result = resp.json()

print("Result:", json.dumps(result, ensure_ascii=False))
