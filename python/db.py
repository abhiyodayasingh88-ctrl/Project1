import sqlite3
conn = sqlite3.connect('C:\Users\abhiy\OneDrive\Pictures\文件\Html\python\users.db.db')
#  cursor = conn.cursor
cursor = conn.cursor()
cursor.execute("Select * From users")
print(cursor.fetchall())