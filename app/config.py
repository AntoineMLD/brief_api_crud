from pydantic_settings import BaseSettings, Field
from typing import Optional
import os

class Settings(BaseSettings):
    # Champs pour la configuration générale
    app_name: str = "API CRUD avec Authentification"
    secret_key: str  # Clé secrète pour JWT
    algorithm: str = "HS256"  # Algorithme pour JWT
    access_token_expire_minutes: int = 30  # Durée de validité des tokens en minutes

    # Informations pour la base de données
    server_name: str  # Nom du serveur
    bdd_name: str  # Nom de la base de données
    user: str  # Utilisateur pour la base de données
    mdp: str  # Mot de passe pour la base de données
    port: int  # Port utilisé par le serveur

    # Mot de passe hashé pour l'utilisateur (authentification)
    hashed_password: str  # Mot de passe hashé récupéré depuis .env

    @property
    def database_url(self) -> str:
        """Génère dynamiquement l'URL de connexion à la base de données."""
        return (
            f"mssql+pyodbc://{self.user}:{self.mdp}@{self.server_name}:{self.port}/"
            f"{self.bdd_name}?driver=ODBC+Driver+18+for+SQL+Server"
        ).replace(" ", "+")

    class Config:
        # Charge les variables d'environnement depuis le fichier .env
        env_file = ".env"
        env_file_encoding = 'utf-8'

    def validate(self):
        """
        Valide les informations essentielles et l'intégrité des variables d'environnement.
        Cette méthode est appelée après l'instanciation des paramètres.
        """
        # Vérifie si la clé secrète est présente et valide
        if not self.secret_key:
            raise ValueError("La clé secrète 'secret_key' est manquante dans le fichier .env.")
        
        # Vérifie si les informations pour la base de données sont définies
        if not all([self.server_name, self.bdd_name, self.user, self.mdp]):
            raise ValueError("Certaines informations essentielles pour la base de données manquent dans le fichier .env.")
        
        # Vérifie la configuration du mot de passe haché
        if not self.hashed_password:
            raise ValueError("Le mot de passe haché 'hashed_password' est manquant dans le fichier .env.")


settings = Settings()


settings.validate()
