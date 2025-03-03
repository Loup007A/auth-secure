import sqlite3

conn = sqlite3.connect("database/users.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}, Password Hash: {user[2]}")

conn.close()
