from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# Vérifier si le dossier existe
if not os.path.exists("keys"):
    os.makedirs("keys")

# Générer une paire de clés RSA (2048 bits)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Sauvegarder la clé privée
with open("keys/private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Sauvegarder la clé publique
public_key = private_key.public_key()
with open("keys/public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("✅ Clés RSA générées avec succès !")
