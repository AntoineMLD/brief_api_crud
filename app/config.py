from pydantic_settings import BaseSettings


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
        env_file = ".env"  # Fichier contenant les variables d'environnement


# Instancier les paramètres pour les utiliser dans toute l'application
settings = Settings()
