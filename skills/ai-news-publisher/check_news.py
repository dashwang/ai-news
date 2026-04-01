#!/usr/bin/env python3
import sqlite3
conn = sqlite3.connect('data/news.db')
cur = conn.cursor()
cur.execute("SELECT source, COUNT(*) FROM news WHERE date='2026-03-31' GROUP BY source")
for row in cur.fetchall():
    print(f"{row[0]}: {row[1]}")
conn.close()
