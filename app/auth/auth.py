import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta

# Charger les variables d'environnement
load_dotenv()

# Récupération de la clé secrète et du mot de passe haché depuis le fichier .env
SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
HASHED_PASSWORD = os.getenv("HASHED_PASSWORD")

# Vérification des valeurs nécessaires
if not HASHED_PASSWORD:
    raise ValueError("HASHED_PASSWORD n'est pas défini dans le fichier .env.")

# Gestion des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dépendance OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Vérifier le mot de passe
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Authentifier un utilisateur
def authenticate_user(username: str, password: str) -> bool:
    if username != "testuser":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not verify_password(password, HASHED_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return True

# Créer un token d'accès
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Génère un token JWT.

    Args:
        data (dict): Données à encoder dans le token.
        expires_delta (timedelta, optional): Durée de validité du token.

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
    Dépendance pour vérifier et obtenir l'utilisateur actuel.

    Args:
        token (str): Token JWT.

    Returns:
        dict: Détails de l'utilisateur.

    Raises:
        HTTPException: Si le token est invalide ou expiré.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if username != "testuser":
        raise credentials_exception
    return {"username": username}
