from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    # Champs pour la configuration générale
    app_name: str = "API CRUD avec Authentification"
    secret_key: str = Field(..., env="SECRET_KEY")  # Clé secrète pour JWT
    algorithm: str = Field(default="HS256", env="ALGORITHM")  # Algorithme pour JWT
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")  # Durée de validité des tokens

    # Informations pour la base de données
    server_name: str = Field(..., env="SERVER_NAME")  # Nom du serveur
    bdd_name: str = Field(..., env="BDD_NAME")  # Nom de la base de données
    user: str = Field(..., env="USER")  # Utilisateur pour la base de données
    mdp: str = Field(..., env="MDP")  # Mot de passe pour la base de données
    port: int = Field(default=1433, env="PORT")  # Port utilisé par le serveur

    # Mot de passe hashé pour l'utilisateur (authentification)
    hashed_password: str = Field(..., env="HASHED_PASSWORD")  # Mot de passe hashé récupéré depuis .env

    @property
    def database_url(self) -> str:
        return (
            f"mssql+pyodbc://{self.user}:{self.mdp}@{self.server_name}:{self.port}/"
            f"{self.bdd_name}?driver=ODBC+Driver+18+for+SQL+Server&timeout=60"
        ).replace(" ", "+")


    class Config:
        # Charge les variables d'environnement depuis le fichier .env
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

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
