from passlib.context import CryptContext
import os
from dotenv import load_dotenv, dotenv_values

# Recharge le fichier .env explicitement
dotenv_values(".env")  # Charge les valeurs depuis le fichier .env
load_dotenv(override=True)

# Crée un contexte pour bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Récupére le mot de passe haché depuis le .env
hashed_password = os.getenv("HASHED_PASSWORD").strip()
plain_password = "password"

print(f"Mot de passe en clair : {plain_password} (longueur : {len(plain_password)})")
print(f"Hachage depuis .env : {hashed_password} (longueur : {len(hashed_password)})")
print(f"Correspondance : {pwd_context.verify(plain_password, hashed_password)}")
