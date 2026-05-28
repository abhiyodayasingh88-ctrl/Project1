import sqlite3

# Database connect
conn = sqlite3.connect('users.db')

# Cursor create
cursor = conn.cursor()

# Saara data fetch karo
cursor.execute("SELECT * FROM users")

# Rows store karo
rows = cursor.fetchall()

# Print karo
for row in rows:
    print(row)

# Connection close
conn.close()