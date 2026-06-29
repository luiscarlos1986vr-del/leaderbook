import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Obtener URL de la base de datos (debe funcionar local y en Render)
DATABASE_URL = os.getenv('DATABASE_URL')

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Modelo de Usuario
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Modelo de Perfil CT
class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, unique=True, index=True)
    ct_principal = Column(String)    # A, N, E, M, H, P, O
    ct_modifier = Column(String)
    ct_matizer = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Modelo de Registro Semanal
class WeeklyRecord(Base):
    __tablename__ = "weekly_records"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    week_number = Column(Integer)
    date = Column(DateTime, default=datetime.now)
    
    # Secciones del mapa
    potential_personal = Column(Text)
    potential_professional = Column(Text)
    blindspot_personal = Column(Text)
    blindspot_professional = Column(Text)
    adaptation_personal = Column(Text)
    adaptation_professional = Column(Text)
    habit_strength = Column(Text)
    habit_challenge = Column(Text)
    habit_practice = Column(Text)
    
    # Indicadores (1-5)
    analysis_score = Column(Integer)
    flexibility_score = Column(Integer)
    delegation_score = Column(Integer)
    communication_score = Column(Integer)
    development_score = Column(Integer)
    serenity_score = Column(Integer)
    balance_score = Column(Integer)
    
    # Retroalimentación IA
    ai_feedback = Column(Text, nullable=True)
    ct_profile = Column(Text, nullable=True)  # Guardar perfil CT para contexto
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Función para obtener sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para crear las tablas (¡Esta es la clave!)
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente")
