import uuid
import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import WeeklyRecord

def get_week_number(date):
    """Calcula el número de semana del año"""
    start_date = datetime(date.year, 1, 1)
    days = (date - start_date).days
    return (days + start_date.weekday() + 1) // 7 + 1

def create_record(db: Session, user_id: str, data: dict):
    """Crea un nuevo registro semanal"""
    week_number = get_week_number(datetime.now())
    
    # Verificar si ya existe registro esta semana
    existing = db.query(WeeklyRecord).filter(
        WeeklyRecord.user_id == user_id,
        WeeklyRecord.week_number == week_number
    ).first()
    
    if existing:
        raise ValueError(f"Ya existe un registro para la semana {week_number}")
    
    # Extraer campos extra que no están en el modelo
    extra_fields = ['evidence', 'blindspots', 'communication']
    extra_data = {k: data.pop(k) for k in extra_fields if k in data}
    
    # Guardar campos extra como JSON en ai_feedback (temporal)
    if extra_data:
        data['ai_feedback'] = json.dumps(extra_data)
    
    record = WeeklyRecord(
        id=str(uuid.uuid4()),
        user_id=user_id,
        week_number=week_number,
        date=datetime.now(),
        **data
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return record