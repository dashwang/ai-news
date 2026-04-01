import sqlite3
conn = sqlite3.connect('data/news.db')
cur = conn.cursor()
cur.execute("SELECT DISTINCT date FROM news ORDER BY date DESC")
for row in cur.fetchall():
    print(row[0])
conn.close()
