from sqlalchemy.orm import Session
from app.models.database import WeeklyRecord

def calculate_stats(db: Session, user_id: str):
    """
    Calcula estadísticas completas del usuario para el dashboard.
    """
    records = db.query(WeeklyRecord).filter(
        WeeklyRecord.user_id == user_id
    ).order_by(WeeklyRecord.date.desc()).all()
    
    if not records:
        return {
            'total_weeks': 0,
            'averages': {},
            'trends': [],
            'latest': None
        }
    
    total = len(records)
    
    # Calcular promedios
    indicators = ['analysis', 'flexibility', 'delegation', 'communication', 
                  'development', 'serenity', 'balance']
    
    averages = {}
    for indicator in indicators:
        score_attr = f'{indicator}_score'
        values = [getattr(r, score_attr) for r in records]
        averages[indicator] = sum(values) / total if values else 0
    
    # Preparar datos de tendencias (orden ascendente para gráficos)
    trends = []
    for record in sorted(records, key=lambda x: x.date):
        trend = {
            'week': record.week_number,
            'date': record.date.strftime('%Y-%m-%d')
        }
        for indicator in indicators:
            score_attr = f'{indicator}_score'
            trend[indicator] = getattr(record, score_attr)
        trends.append(trend)
    
    return {
        'total_weeks': total,
        'averages': averages,
        'trends': trends,
        'latest': records[0]  # El más reciente
    }