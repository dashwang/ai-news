#!/usr/bin/env python3
"""
Railway 入口脚本
支持 webhook 触发和手动执行
"""

import os
import sys
from fetch_news import main as fetch_main
from publish_wechat import main as publish_main


def handler(event, context):
    """Railway handler - 被定时任务或 webhook 触发"""
    print("🚀 AI News Bot triggered")

    # Step 1: Fetch news
    print("\n[1/2] Fetching news...")
    fetch_success = fetch_main()

    if not fetch_success:
        return {"statusCode": 500, "body": "Failed to fetch news"}

    # Step 2: Publish to WeChat
    print("\n[2/2] Publishing to WeChat...")
    publish_success = publish_main()

    if not publish_success:
        return {"statusCode": 500, "body": "Failed to publish"}

    return {"statusCode": 200, "body": "Success!"}


if __name__ == "__main__":
    # 手动执行
    print("Running fetch news...")
    fetch_main()
    print("\nRunning publish...")
    publish_main()
