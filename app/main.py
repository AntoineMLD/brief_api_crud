from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from typing import List
from app.auth.auth import create_access_token, authenticate_user, get_current_user
from app.database import get_session
from app.models import Product, ProductCreate

# Initialisation de l'application FastAPI
app = FastAPI(
    title="API CRUD avec Authentification",
    description="""
API pour gérer les produits avec un système d'authentification sécurisé basé sur OAuth2 et JWT.
### Fonctionnalités :
1. **Authentification** : Génération de tokens pour sécuriser les routes.
2. **Gestion des produits** :
    - Lister les produits.
    - Consulter un produit spécifique.
    - Ajouter un produit.
    - Modifier un produit existant.
    - Supprimer un produit.
""",
    version="1.0.0",
)

# Durée d'expiration des tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected/", response_model=dict)
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user['username']}!"}
@app.get("/products/", response_model=List[Product], tags=["Produits"])
async def list_products(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """
    Liste tous les produits disponibles.

    - **Token requis** : Oui.
    """
    statement = select(Product)
    results = session.exec(statement).all()
    return results

@app.get("/products/{product_id}", response_model=Product, tags=["Produits"])
async def get_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """
    Consulte un produit spécifique par son ID.

    - **product_id** : ID du produit.
    - **Token requis** : Oui.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product

@app.post("/products/", response_model=Product, tags=["Produits"])
async def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """
    Ajoute un nouveau produit.

    - **Body** : Détails du produit à créer.
    - **Token requis** : Oui.
    """
    new_product = Product.from_orm(product)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@app.put("/products/{product_id}", response_model=Product, tags=["Produits"])
async def update_product(
    product_id: int,
    product: ProductCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """
    Met à jour un produit existant.

    - **product_id** : ID du produit à modifier.
    - **Body** : Détails du produit à mettre à jour.
    - **Token requis** : Oui.
    """
    existing_product = session.get(Product, product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(existing_product, key, value)
    
    session.add(existing_product)
    session.commit()
    session.refresh(existing_product)
    return existing_product

@app.delete("/products/{product_id}", response_model=dict, tags=["Produits"])
async def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """
    Supprime un produit existant.

    - **product_id** : ID du produit à supprimer.
    - **Token requis** : Oui.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    session.delete(product)
    session.commit()
    return {"message": f"Produit {product_id} supprimé avec succès"}
