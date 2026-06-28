# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 13:30:59 2026

@author: user1
"""

import bcrypt
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import User

# Hashear contraseña
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Verificar contraseña
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Crear usuario
def create_user(db: Session, email: str, name: str, password: str):
    # Verificar si el email ya existe
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None, "El email ya está registrado"
    
    # Crear nuevo usuario
    user = User(
        id=str(uuid.uuid4()),
        email=email,
        name=name,
        password_hash=hash_password(password),
        created_at=datetime.now()
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, None

# Autenticar usuario
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None, "Usuario no encontrado"
    
    if not verify_password(password, user.password_hash):
        return None, "Contraseña incorrecta"
    
    return user, None

# Obtener usuario por ID
def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()