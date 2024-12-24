import os
from passlib.context import CryptContext
from dotenv import load_dotenv

# Charge explicitement les variables d'environnement
load_dotenv()

# Crée un contexte pour bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si le mot de passe en texte clair correspond au mot de passe haché.

    Args:
        plain_password (str): Mot de passe en texte clair.
        hashed_password (str): Mot de passe haché à vérifier.

    Returns:
        bool: True si les mots de passe correspondent, sinon False.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        raise ValueError(f"Erreur lors de la vérification du mot de passe : {str(e)}")

if __name__ == "__main__":
    # Charge le mot de passe haché depuis les variables d'environnement
    hashed_password = os.getenv("HASHED_PASSWORD")
    if not hashed_password:
        raise ValueError("La variable d'environnement HASHED_PASSWORD est manquante.")

    # Mot de passe en clair pour la vérification
    plain_password = "password"  

    # Affiche les informations
    print(f"Mot de passe en clair : {plain_password} (longueur : {len(plain_password)})")
    print(f"Hachage depuis .env : {hashed_password} (longueur : {len(hashed_password)})")

    # Vérifie le mot de passe
    is_verified = verify_password(plain_password, hashed_password)
    print(f"Correspondance : {is_verified}")
