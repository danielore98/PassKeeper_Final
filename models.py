# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # Almacenamos la contraseña sin cifrar, para autenticación

    # Relación con contraseñas
    passwords = relationship("Password", back_populates="owner")

class Password(Base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # Nombre de la contraseña
    username = Column(String)  # Nombre de usuario asociado
    encrypted_password = Column(String)  # Contraseña encriptada
    category = Column(String)  # Categoría de la contraseña
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relación inversa con el usuario
    owner = relationship("User", back_populates="passwords")
