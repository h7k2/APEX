from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, products, orders

# Création des tables au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="APEX Sport & Tech — API",
    description="Back-end e-commerce: produits, commandes, authentification, emails",
    version="1.0.0"
)

# Autoriser le front-end à communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En prod, remplacer par votre domaine
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes
app.include_router(auth.router,     prefix="/auth",     tags=["Authentification"])
app.include_router(products.router, prefix="/products", tags=["Produits"])
app.include_router(orders.router,   prefix="/orders",   tags=["Commandes"])

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "APEX API opérationnelle 🚀"}
