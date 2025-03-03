# 🔐 Auth-Secure : Système d'authentification sécurisé

Ce projet implémente une **authentification sécurisée** avec :
- 🏗️ **Flask** (Backend API)
- 🔐 **RSA + Cryptography** (Sécurisation des mots de passe)
- 🛡️ **JWT + IDS** (Détection d'intrusion)
- 🗄️ **SQLite** (Stockage des utilisateurs)

## 🚀 Installation
```bash
git clone https://github.com/TON-USERNAME/auth-secure.git
cd auth-secure
pip install -r requirements.txt
python generate_keys.py  # Génération des clés RSA
python database_setup.py  # Initialisation de la base de données
python app.py  # Démarrer le serveur
