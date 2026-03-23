# APEX — Back-end FastAPI

API e-commerce complète pour la boutique APEX Sport & Tech.

## 🚀 Installation

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer le serveur
uvicorn main:app --reload
```

L'API sera disponible sur : http://localhost:8000

## 📖 Documentation interactive

FastAPI génère automatiquement une doc interactive :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc**       : http://localhost:8000/redoc

## 📁 Structure

```
apex-backend/
├── main.py            # Point d'entrée FastAPI
├── database.py        # Config SQLAlchemy + SQLite
├── models.py          # Tables : User, Product, Order, OrderItem
├── email_service.py   # Envoi d'emails (bienvenue, confirmation)
├── requirements.txt
└── routers/
    ├── auth.py        # POST /auth/register, /auth/login, GET /auth/me
    ├── products.py    # GET/POST/PUT/DELETE /products
    └── orders.py      # POST/GET /orders
```

## 🔑 Routes principales

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| POST | /auth/register | Créer un compte | — |
| POST | /auth/login | Connexion → JWT | — |
| GET  | /auth/me | Profil connecté | ✅ |
| GET  | /products | Liste produits | — |
| GET  | /products/{id} | Détail produit | — |
| POST | /products | Créer produit | 🔐 Admin |
| PUT  | /products/{id} | Modifier produit | 🔐 Admin |
| DELETE | /products/{id} | Supprimer produit | 🔐 Admin |
| POST | /orders | Passer commande | ✅ |
| GET  | /orders/my | Mes commandes | ✅ |
| PATCH | /orders/{id}/status | Changer statut | 🔐 Admin |

## ✉️ Configuration emails

Dans `email_service.py`, remplacer :
```python
SMTP_USER     = "votre-email@gmail.com"
SMTP_PASSWORD = "votre-mot-de-passe-app"   # Mot de passe d'application Gmail
```

## ⚙️ Passage en production

1. Remplacer SQLite par PostgreSQL dans `database.py`
2. Changer `SECRET_KEY` dans `routers/auth.py`
3. Restreindre `allow_origins` dans `main.py`
4. Déployer sur Railway, Render ou un VPS
