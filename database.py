# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Conexión a la base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

# Sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Inicializa las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Devuelve una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
