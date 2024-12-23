# API CRUD avec Authentification

Cette API est conçue pour gérer des produits dans une base de données en utilisant FastAPI. Elle inclut une authentification basée sur OAuth2 avec JWT pour sécuriser les routes.

## Fonctionnalités principales

- Génération de tokens d'accès (`/token`).
- Gestion des produits (CRUD) :
  - **Lister les produits** : `GET /products/`
  - **Consulter un produit spécifique** : `GET /products/{product_id}`
  - **Créer un nouveau produit** : `POST /products/`
  - **Mettre à jour un produit existant** : `PUT /products/{product_id}`
  - **Supprimer un produit** : `DELETE /products/{product_id}`

---

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone <url_du_repo>
   cd <nom_du_projet>
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate    # Sur Linux/Mac
   venv\Scripts\activate     # Sur Windows
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement** :
   Créez un fichier `.env` à la racine du projet et ajoutez-y :
   ```env
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   SERVER_NAME=your_server_name
   BDD_NAME=your_database_name
   USER=your_database_user
   MDP=your_database_password
   PORT=your_database_port
   HASHED_PASSWORD=hashed_password_for_testuser
   ```

5. **Lancer l'application** :
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Utilisation de l'API

### 1. **Authentification** : `POST /token`
- **Description** : Obtenir un token d'accès.
- **Exemple de corps** :
  ```json
  {
    "username": "testuser",
    "password": "password"
  }
  ```

- **Réponse** :
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
    "token_type": "bearer"
  }
  ```

### 2. **Lister les produits** : `GET /products/`
- **Description** : Récupère la liste des produits.
- **Exemple de réponse** :
  ```json
  [
    {
      "ProductID": 1,
      "Name": "Produit 1",
      "ProductNumber": "P001",
      "ListPrice": 15.0,
      "ModifiedDate": "2024-01-01T12:00:00"
    },
    {
      "ProductID": 2,
      "Name": "Produit 2",
      "ProductNumber": "P002",
      "ListPrice": 20.0,
      "ModifiedDate": "2024-01-01T12:00:00"
    }
  ]
  ```

### 3. **Consulter un produit spécifique** : `GET /products/{product_id}`
- **Description** : Récupère les détails d'un produit spécifique.
- **Exemple de réponse** :
  ```json
  {
    "ProductID": 1,
    "Name": "Produit 1",
    "ProductNumber": "P001",
    "ListPrice": 15.0,
    "ModifiedDate": "2024-01-01T12:00:00"
  }
  ```

### 4. **Créer un nouveau produit** : `POST /products/`
- **Description** : Ajoute un nouveau produit.
- **Exemple de corps** :
  ```json
  {
    "Name": "Produit 3",
    "ProductNumber": "P003",
    "ListPrice": 25.0,
    "SellStartDate": "2024-01-01T12:00:00"
  }
  ```

- **Réponse** :
  ```json
  {
    "ProductID": 3,
    "Name": "Produit 3",
    "ProductNumber": "P003",
    "ListPrice": 25.0,
    "SellStartDate": "2024-01-01T12:00:00",
    "ModifiedDate": "2024-01-01T12:00:00"
  }
  ```

---

## Documentation interactive

Une documentation interactive est disponible à l'adresse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## Tests

1. **Tester l'API localement** :
   - Utiliser un outil comme Postman ou cURL pour tester les endpoints.
   - Ajouter un token valide dans les en-têtes pour les routes protégées :
     ```
     Authorization: Bearer <access_token>
     ```

2. **Exemple avec cURL** :
   ```bash
   curl -X GET "http://127.0.0.1:8000/products/" -H "Authorization: Bearer <access_token>"
   ```

---

## Structure du projet

```
project/
│
├── app/
│   ├── main.py              # Entrée principale de l'application
│   ├── config.py            # Configuration de l'application
│   ├── database.py          # Connexion à la base de données
│   ├── models.py            # Définition des modèles SQLModel
│   ├── auth/
│   │   ├── auth.py          # Gestion des authentifications
│   ├── routes/
│       ├── products.py      # Routes liées aux produits
│
├── .env                     # Fichier d'environnement
├── requirements.txt         # Dépendances du projet
└── README.md                # Documentation du projet
```
