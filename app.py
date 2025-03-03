from flask import Flask, request, jsonify
import sqlite3
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

app = Flask(__name__)
SECRET_KEY = "supersecretkey"

# Charger les clés RSA
with open("keys/private_key.pem", "rb") as f:
    PRIVATE_KEY = load_pem_private_key(f.read(), password=None)
with open("keys/public_key.pem", "rb") as f:
    PUBLIC_KEY = load_pem_public_key(f.read())

# Route d'inscription
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = generate_password_hash(data["password"])

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
        conn.commit()
        return jsonify({"message": "Utilisateur enregistré avec succès !"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Nom d'utilisateur déjà pris"}), 400
    finally:
        conn.close()

# Route de connexion
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[0], password):
        token = jwt.encode({"user": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                           SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token}), 200
    return jsonify({"error": "Identifiants incorrects"}), 401

# Route pour obtenir la clé publique
@app.route("/get_public_key", methods=["GET"])
def get_public_key():
    return jsonify({"public_key": PUBLIC_KEY.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")})

if __name__ == "__main__":
    app.run(debug=True)
