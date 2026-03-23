from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import get_db
from models import Order, OrderItem, Product, OrderStatus
from routers.auth import get_current_user, require_admin
from email_service import send_order_confirmation

router = APIRouter()

# ─── SCHEMAS ────────────────────────────────────────────────────
class CartItem(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[CartItem]
    address: str

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    status: OrderStatus
    total: float
    address: str
    items: List[OrderItemOut]
    class Config:
        from_attributes = True

# ─── ROUTES UTILISATEUR ─────────────────────────────────────────
@router.post("/", response_model=OrderOut, status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Passer une commande depuis le panier."""
    if not data.items:
        raise HTTPException(status_code=400, detail="Le panier est vide")

    total = 0.0
    order_items = []

    for cart_item in data.items:
        product = db.query(Product).filter(Product.id == cart_item.product_id, Product.is_active == True).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produit {cart_item.product_id} introuvable")
        if product.stock < cart_item.quantity:
            raise HTTPException(status_code=400, detail=f"Stock insuffisant pour {product.name}")

        subtotal = product.price * cart_item.quantity
        total += subtotal
        product.stock -= cart_item.quantity  # Décrémenter le stock

        order_items.append(OrderItem(
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=product.price
        ))

    order = Order(
        user_id=current_user.id,
        total=round(total, 2),
        address=data.address,
        items=order_items
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Email de confirmation
    send_order_confirmation(current_user.email, current_user.full_name, order.id, total)

    return order

@router.get("/my", response_model=List[OrderOut])
def my_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Historique des commandes de l'utilisateur connecté."""
    return db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Détail d'une commande (propriétaire ou admin)."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès interdit")
    return order

# ─── ROUTES ADMIN ───────────────────────────────────────────────
@router.get("/", response_model=List[OrderOut])
def all_orders(db: Session = Depends(get_db), _=Depends(require_admin)):
    """[Admin] Toutes les commandes."""
    return db.query(Order).order_by(Order.created_at.desc()).all()

@router.patch("/{order_id}/status", response_model=OrderOut)
def update_status(order_id: int, status: OrderStatus, db: Session = Depends(get_db), _=Depends(require_admin)):
    """[Admin] Modifier le statut d'une commande."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    order.status = status
    db.commit()
    db.refresh(order)
    return order
