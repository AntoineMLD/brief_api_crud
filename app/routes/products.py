from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import Product, ProductCreate
from app.auth.auth import get_current_user
from typing import List

router = APIRouter()

# Récupére la liste des produits
@router.get("/", response_model=List[Product], summary="Lister les produits")
async def list_products(
    session: Session = Depends(get_session), 
    user=Depends(get_current_user)
):
    try:
        # Récupére tous les produits depuis la base de données
        statement = select(Product)
        products = session.exec(statement).all()

        # Vérification si des produits ont été trouvés
        if not products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aucun produit trouvé"
            )
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des produits : {str(e)}"
        )

# Crée un nouveau produit
@router.post("/", response_model=Product, summary="Créer un produit")
async def create_product(
    product: ProductCreate, 
    session: Session = Depends(get_session), 
    user=Depends(get_current_user)
):
    try:
        # Vérife si l'utilisateur a les droits nécessaires
        if not user or not user.get('is_admin', False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous n'avez pas les droits pour créer un produit"
            )

        # Création d'un nouveau produit dans la base de données
        new_product = Product.from_orm(product)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        return new_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du produit : {str(e)}"
        )
