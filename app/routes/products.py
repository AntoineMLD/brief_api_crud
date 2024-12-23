from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Product, ProductCreate
from app.auth.auth import get_current_user
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Product], summary="Lister les produits")
async def list_products(session: Session = Depends(get_session), user=Depends(get_current_user)):
    statement = select(Product)
    return session.exec(statement).all()

@router.post("/", response_model=Product, summary="Créer un produit")
async def create_product(product: ProductCreate, session: Session = Depends(get_session), user=Depends(get_current_user)):
    new_product = Product.from_orm(product)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product
