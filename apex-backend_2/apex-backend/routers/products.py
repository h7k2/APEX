from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import Product
from routers.auth import get_current_user, require_admin

router = APIRouter()

# ─── SCHEMAS ────────────────────────────────────────────────────
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    stock: int = 0
    category: str
    emoji: str = "📦"
    badge: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    emoji: Optional[str] = None
    badge: Optional[str] = None
    is_active: Optional[bool] = None

class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    original_price: Optional[float]
    stock: int
    category: str
    emoji: str
    badge: Optional[str]
    is_active: bool
    class Config:
        from_attributes = True

# ─── ROUTES PUBLIQUES ───────────────────────────────────────────
@router.get("/", response_model=List[ProductOut])
def list_products(
    category: Optional[str] = Query(None, description="Filtrer par catégorie"),
    search: Optional[str]   = Query(None, description="Recherche par nom"),
    db: Session = Depends(get_db)
):
    """Liste tous les produits actifs, avec filtres optionnels."""
    q = db.query(Product).filter(Product.is_active == True)
    if category:
        q = q.filter(Product.category == category)
    if search:
        q = q.filter(Product.name.ilike(f"%{search}%"))
    return q.all()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Détail d'un produit."""
    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return product

# ─── ROUTES ADMIN ───────────────────────────────────────────────
@router.post("/", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    """[Admin] Créer un nouveau produit."""
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    """[Admin] Modifier un produit."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    """[Admin] Désactiver un produit (soft delete)."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    product.is_active = False
    db.commit()
