import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("database/users.db")
cursor = conn.cursor()

# Création de la table des utilisateurs
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Base de données SQLite initialisée !")
