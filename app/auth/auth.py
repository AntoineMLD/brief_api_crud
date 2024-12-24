import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional

# Charge les variables d'environnement
load_dotenv()

# Récupére des variables depuis le fichier .env 
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
HASHED_PASSWORD = os.getenv("HASHED_PASSWORD")

# Vérifie la présence des variables d'environnement critiques
if not SECRET_KEY:
    raise ValueError("La variable SECRET_KEY n'est pas définie dans le fichier .env.")
if not HASHED_PASSWORD:
    raise ValueError("La variable HASHED_PASSWORD n'est pas définie dans le fichier .env.")

# Gestion des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dépendance OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Vérifie si le mot de passe est correct
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si le mot de passe en texte clair correspond au mot de passe haché.

    Args:
        plain_password (str): Mot de passe en texte clair.
        hashed_password (str): Mot de passe haché.

    Returns:
        bool: True si le mot de passe est valide, sinon False.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Authentifie un utilisateur
def authenticate_user(username: str, password: str) -> bool:
    """
    Authentifie l'utilisateur en vérifiant le nom d'utilisateur et le mot de passe.

    Args:
        username (str): Nom d'utilisateur.
        password (str): Mot de passe.

    Returns:
        bool: True si l'utilisateur est authentifié avec succès.

    Raises:
        HTTPException: Si le nom d'utilisateur ou le mot de passe est incorrect.
    """
    if username != "testuser":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur incorrect",
        )
    if not verify_password(password, HASHED_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe incorrect",
        )
    return True

# Crée un token d'accès
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Génère un token JWT pour l'utilisateur.

    Args:
        data (dict): Données à encoder dans le token.
        expires_delta (Optional[timedelta]): Durée de validité du token.

    Returns:
        str: Token JWT encodé.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dépendance pour obtenir l'utilisateur actuel
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Vérifie le token JWT et retourne les détails de l'utilisateur actuel.

    Args:
        token (str): Token JWT.

    Returns:
        dict: Détails de l'utilisateur connecté.

    Raises:
        HTTPException: Si le token est invalide ou expiré.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Décodage du token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Vérifie que l'utilisateur est valide
    if username != "testuser":
        raise credentials_exception
    
    return {"username": username}
