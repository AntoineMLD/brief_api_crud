from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

plain_password = "password"  # Le mot de passe à hacher
hashed_password = pwd_context.hash(plain_password)

print(f"Nouveau hachage généré : {hashed_password}")
