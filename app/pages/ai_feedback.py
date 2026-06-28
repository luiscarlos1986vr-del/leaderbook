import streamlit as st
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import get_db
from app.models.database import WeeklyRecord
from app.services.ai_service import get_ai_feedback

def show_ai_feedback():
    if not st.session_state.get('authenticated', False):
        st.warning("⚠️ Por favor inicia sesión")
        st.session_state.page = "main"
        st.rerun()
        return
    
    st.title("🧠 Retroalimentación Personalizada")
    st.caption("Basado en tu perfil CT: Autístico-Normaloide con matiz Epileptoide")
    st.markdown("""
    *"Mi objetivo no es cambiar quién soy, sino utilizar conscientemente mis fortalezas 
    y desarrollar las capacidades que las complementan."*
    """)
    
    db = next(get_db())
    
    # Obtener el último registro del usuario
    latest_record = db.query(WeeklyRecord).filter(
        WeeklyRecord.user_id == st.session_state.user['id']
    ).order_by(WeeklyRecord.date.desc()).first()
    
    if not latest_record:
        st.info("📝 Aún no tienes registros. Guarda tu primer registro semanal para recibir retroalimentación.")
        return
    
    st.success(f"📊 Analizando registro de la semana {latest_record.week_number}")
    
    # Mostrar un resumen del registro
    with st.expander("📋 Ver mi registro (para contexto)", expanded=False):
        st.markdown(f"""
        **Personal:** {latest_record.potential_personal[:200]}...
        **Profesional:** {latest_record.potential_professional[:200]}...
        **Punto ciego personal:** {latest_record.blindspot_personal[:200]}...
        **Punto ciego profesional:** {latest_record.blindspot_professional[:200]}...
        """)
    
    # Botón único para generar retroalimentación (siempre reflexiva, temp 0.2)
    if st.button("🎯 Generar Análisis Profundo (Temp 0.2)", use_container_width=True):
        with st.spinner("🧠 Analizando tu registro desde tu perfil CT..."):
            # Preparar datos para la IA
            record_data = {
                'potential_personal': latest_record.potential_personal,
                'potential_professional': latest_record.potential_professional,
                'blindspot_personal': latest_record.blindspot_personal,
                'blindspot_professional': latest_record.blindspot_professional,
                'adaptation_personal': latest_record.adaptation_personal,
                'adaptation_professional': latest_record.adaptation_professional,
                'habit_strength': latest_record.habit_strength,
                'habit_challenge': latest_record.habit_challenge,
                'habit_practice': latest_record.habit_practice,
                'analysis_score': latest_record.analysis_score,
                'flexibility_score': latest_record.flexibility_score,
                'delegation_score': latest_record.delegation_score,
                'communication_score': latest_record.communication_score,
                'development_score': latest_record.development_score,
                'serenity_score': latest_record.serenity_score,
                'balance_score': latest_record.balance_score,
                'evidence': '',
                'blindspots': {},
                'communication': ''
            }
            
            # Intentar extraer campos extra del ai_feedback (guardados como JSON)
            if latest_record.ai_feedback:
                try:
                    extra = json.loads(latest_record.ai_feedback)
                    record_data['evidence'] = extra.get('evidence', '')
                    record_data['blindspots'] = extra.get('blindspots', {})
                    record_data['communication'] = extra.get('communication', '')
                except:
                    pass
            
            # Generar feedback (sin modo, ya no se usa)
            feedback = get_ai_feedback(record_data)
            
            # Mostrar feedback
            st.markdown("---")
            st.markdown("### 🧠 Análisis Personalizado (Basado en tu CT)")
            st.markdown(feedback)
            
            # Guardar el feedback en la base de datos
            latest_record.ai_feedback = feedback
            db.commit()
            st.success("✅ Análisis guardado en tu historial")
            st.balloons()
    
    # Mostrar feedback anterior si existe
    if latest_record.ai_feedback and "Error" not in latest_record.ai_feedback:
        with st.expander("📜 Ver mi último análisis guardado", expanded=False):
            st.markdown(latest_record.ai_feedback)