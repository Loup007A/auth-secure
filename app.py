from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session

app = Flask(__name__)

# Configuration de la session Flask
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# 📌 Route pour afficher la page principale (inscription & connexion)
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# 📌 Route pour inscrire un utilisateur
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = generate_password_hash(data["password"])  # Hachage du mot de passe

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

# 📌 Route pour récupérer la liste des utilisateurs
@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    users = [{"id": row[0], "username": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)

# 📌 Route pour se connecter
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
        session["user_id"] = user[0]  # Stocker l'ID utilisateur dans la session
        return jsonify({"message": "Connexion réussie !"}), 200
    return jsonify({"error": "Identifiants incorrects"}), 401

# 📌 Route pour se déconnecter
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))

# 📌 Route du tableau de bord après connexion
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("home"))
    return render_template("dashboard.html")

# 📌 Route pour récupérer l'utilisateur connecté
@app.route("/session", methods=["GET"])
def session_info():
    if "user_id" in session:
        conn = sqlite3.connect("database/users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],))
        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({"username": user[0]})
    return jsonify({"error": "Non connecté"}), 401


if __name__ == "__main__":
    app.run(debug=True)
