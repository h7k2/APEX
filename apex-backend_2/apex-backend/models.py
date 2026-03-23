from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class OrderStatus(str, enum.Enum):
    pending   = "pending"
    confirmed = "confirmed"
    shipped   = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

# ─── UTILISATEUR ────────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, unique=True, index=True, nullable=False)
    full_name  = Column(String, nullable=False)
    hashed_pw  = Column(String, nullable=False)
    is_active  = Column(Boolean, default=True)
    is_admin   = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    orders = relationship("Order", back_populates="user")

# ─── PRODUIT ────────────────────────────────────────────────────
class Product(Base):
    __tablename__ = "products"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False)
    description  = Column(Text)
    price        = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)
    stock        = Column(Integer, default=0)
    category     = Column(String, index=True)
    emoji        = Column(String, default="📦")
    badge        = Column(String, nullable=True)   # "new", "sale", "hot"
    is_active    = Column(Boolean, default=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    order_items = relationship("OrderItem", back_populates="product")

# ─── COMMANDE ───────────────────────────────────────────────────
class Order(Base):
    __tablename__ = "orders"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    status     = Column(Enum(OrderStatus), default=OrderStatus.pending)
    total      = Column(Float, nullable=False)
    address    = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user  = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

# ─── LIGNE DE COMMANDE ──────────────────────────────────────────
class OrderItem(Base):
    __tablename__ = "order_items"

    id         = Column(Integer, primary_key=True, index=True)
    order_id   = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # Prix au moment de l'achat

    order   = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
