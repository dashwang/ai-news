#!/usr/bin/env python3
"""
Translate News Worker - 读取原始新闻，翻译成中文，输出到翻译后文件
"""

import os
import sys
import json
from datetime import datetime

INPUT_FILE = "news_raw.json"
OUTPUT_FILE = "news_translated.json"

LLM_MODEL = os.environ.get("LLM_MODEL", "claude-sonnet-4-20250514")


def translate_with_llm(title: str, summary: str) -> dict:
    """使用 Claude Code CLI 翻译标题和摘要"""
    import subprocess
    import re

    prompt = f"""翻译以下AI新闻为中文，返回纯JSON：
标题: {title}
摘要: {summary[:500] if summary else "无"}
返回格式: {{"title_zh": "...", "summary_zh": "..."}}"""

    try:
        result = subprocess.run(
            ["claude", "--print", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = result.stdout.strip()

        json_match = re.search(r"\{[^}]+\}", output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        return {"title_zh": title[:50], "summary_zh": summary[:200] if summary else ""}
    except Exception as e:
        print(f"LLM翻译失败: {e}")
        return {"title_zh": title[:50], "summary_zh": summary[:100] if summary else ""}


def main():
    print("=" * 50)
    print("🌐 Translate News Worker Started")
    print(f"Time: {datetime.now()}")
    print("=" * 50)

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file not found: {INPUT_FILE}")
        return False

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        news_items = json.load(f)

    print(f"\n📥 Loaded {len(news_items)} items from {INPUT_FILE}")

    translated_items = []
    for i, item in enumerate(news_items):
        print(f"🌐 Translating [{i + 1}/{len(news_items)}]...", end=" ")

        title = item.get("title", "")
        summary = item.get("summary", "")

        translated = translate_with_llm(title, summary)

        item["title_zh"] = translated.get("title_zh", title)
        item["summary_zh"] = translated.get(
            "summary_zh", summary[:200] if summary else ""
        )
        item["translated_at"] = datetime.now().isoformat()

        translated_items.append(item)
        print(f"✓ {item['title_zh'][:40]}...")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(translated_items, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Saved {len(translated_items)} translated items to {OUTPUT_FILE}")
    print("✨ Translate News Worker Completed!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
