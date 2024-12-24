import os
from passlib.context import CryptContext

# Initialisation du contexte de hachage avec bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """
    Hache un mot de passe en utilisant bcrypt.

    Args:
        plain_password (str): Le mot de passe en texte clair à hacher.

    Returns:
        str: Le mot de passe haché.
    """
    try:
        hashed_password = pwd_context.hash(plain_password)
        return hashed_password
    except Exception as e:
        # Gestion des erreurs pendant le hachage du mot de passe
        raise ValueError(f"Une erreur est survenue lors du hachage du mot de passe : {str(e)}")

if __name__ == "__main__":
    # Exemple de mot de passe à hacher
    plain_password = os.getenv("PLAIN_PASSWORD", "password")  

    if not plain_password:
        raise ValueError("Le mot de passe à hacher n'est pas défini dans les variables d'environnement.")

    hashed_password = hash_password(plain_password)
    print(f"Nouveau hachage généré : {hashed_password}")
