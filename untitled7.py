import sqlite3

conn = sqlite3.connect('my.db')

cursor = conn.execute("""SELECT * FROM books""")

