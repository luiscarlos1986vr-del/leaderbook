# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 13:13:44 2026

@author: user1
"""

from app.models.database import create_tables, get_db
from sqlalchemy.orm import Session

print("🚀 Probando conexión a la base de datos...")

try:
    # Crear tablas
    create_tables()
    print("✅ Conexión exitosa y tablas creadas")
except Exception as e:
    print(f"❌ Error: {e}")