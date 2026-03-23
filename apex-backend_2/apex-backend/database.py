from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite pour le développement (facile, sans installation)
# En production, remplacer par PostgreSQL :
# DATABASE_URL = "postgresql://user:password@localhost/apex_db"
DATABASE_URL = "sqlite:///./apex.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Nécessaire pour SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dépendance FastAPI : ouvre/ferme la session DB automatiquement
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
