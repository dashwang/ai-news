import sqlite3
conn = sqlite3.connect('data/news.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

sources = ['HackerNews', 'ProductHunt', 'TechCrunch', 'TheSequence']
for src in sources:
    cur.execute('SELECT title, url FROM news WHERE source=? AND date="2026-04-01" ORDER BY score DESC LIMIT 8', (src,))
    rows = cur.fetchall()
    print(f'=== {src} ({len(rows)}条) ===')
    for i, r in enumerate(rows, 1):
        print(f'{i}. {r[0]}')
conn.close()
