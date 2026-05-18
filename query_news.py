#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('/root/.openclaw/workspace/ai-news-custom/skills/ai-news-publisher/data/news.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all articles for 2026-04-01 grouped by source
cursor.execute("""
    SELECT source, title, url, summary, score 
    FROM news 
    WHERE date LIKE '2026-04-01%'
    ORDER BY source, score DESC
""")

rows = cursor.fetchall()

# Group by source
sources = {}
for row in rows:
    src = row['source']
    if src not in sources:
        sources[src] = []
    sources[src].append(row['title'])

# Print results
print("=== DATABASE RESULTS (2026-04-01) ===\n")

for src in ['HackerNews', 'ProductHunt', 'TechCrunch', 'TheSequence']:
    print(f"## {src}")
    if src in sources:
        for i, title in enumerate(sources[src], 1):
            print(f"{i}. {title}")
    else:
        print("  (no data)")
    print()

conn.close()