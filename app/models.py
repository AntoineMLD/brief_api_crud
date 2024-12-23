from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

# Modèle de base pour les produits
class ProductBase(SQLModel):
    Name: str
    ProductNumber: str
    Color: Optional[str] = None
    StandardCost: Optional[float] = None
    ListPrice: Optional[float] = None
    Size: Optional[str] = None
    Weight: Optional[float] = None
    ProductCategoryID: Optional[int] = None
    ProductModelID: Optional[int] = None
    SellStartDate: datetime
    SellEndDate: Optional[datetime] = None
    DiscontinuedDate: Optional[datetime] = None
    ThumbnailPhotoFileName: Optional[str] = None
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=datetime)

# Modèle pour la catégorie des produits
class ProductCategory(SQLModel, table=True):
    __tablename__ = "ProductCategory"
    __table_args__ = {"schema": "SalesLT"}

    ProductCategoryID: int = Field(primary_key=True)
    Name: str
    ParentProductCategoryID: Optional[int] = None
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=datetime)

    Products: List["Product"] = Relationship(back_populates="Category")

# Modèle pour le modèle des produits
class ProductModel(SQLModel, table=True):
    __tablename__ = "ProductModel"
    __table_args__ = {"schema": "SalesLT"}

    ProductModelID: int = Field(primary_key=True)
    Name: str
    CatalogDescription: Optional[str] = None
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=datetime)

    Products: List["Product"] = Relationship(back_populates="Model")

# Modèle pour les produits
class Product(ProductBase, table=True):
    __tablename__ = "Product"
    __table_args__ = {"schema": "SalesLT"}

    ProductID: int = Field(primary_key=True)
    ProductCategoryID: Optional[int] = Field(default=None, foreign_key="SalesLT.ProductCategory.ProductCategoryID")
    ProductModelID: Optional[int] = Field(default=None, foreign_key="SalesLT.ProductModel.ProductModelID")

    Category: Optional[ProductCategory] = Relationship(back_populates="Products")
    Model: Optional[ProductModel] = Relationship(back_populates="Products")

# Modèle pour la création et la mise à jour des produits
class ProductCreate(ProductBase):
    SellStartDate: datetime = Field(default_factory=datetime)
    ModifiedDate: datetime = Field(default_factory=datetime)
