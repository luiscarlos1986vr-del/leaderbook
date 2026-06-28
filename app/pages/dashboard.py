import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import get_db
from app.models.database import WeeklyRecord
from app.services.stats_service import calculate_stats

def show_dashboard():
    # Verificar autenticación
    if not st.session_state.get('authenticated', False):
        st.warning("⚠️ Por favor inicia sesión")
        st.session_state.page = "main"
        st.rerun()
        return
    
    db = next(get_db())
    user_id = st.session_state.user['id']
    
    # Obtener estadísticas
    stats = calculate_stats(db, user_id)
    total_semanas = stats['total_weeks']
    
    # --- TÍTULO Y BIENVENIDA ---
    st.title("📊 Tu Dashboard de Desarrollo")
    st.caption(f"Bienvenido de nuevo, {st.session_state.user['name']}")
    
    # Si no hay registros
    if total_semanas == 0:
        st.info("🌱 Aún no tienes registros. ¡Tu primera semana de crecimiento comienza ahora!")
        if st.button("📝 Ir a Nuevo Registro", use_container_width=True):
            st.session_state.page = "new_record"
            st.rerun()
        return
    
    # --- SECCIÓN 1: REFLEXIÓN DE LA SEMANA ---
    promedios = stats['averages']
    promedio_general = sum(promedios.values()) / len(promedios)
    
    # Elegir mensaje con tono paisa (igual que antes)
    if promedio_general >= 4:
        mensaje = """
        Ay, Luis Carlos, ¡qué bonito!  
        Usted está brillando esta semana. Eso de equilibrar el análisis con la acción se le está dando muy bien.  
        Pero no se vaya a descuidar con el perfeccionismo, ¿sí?  
        Un pasito a la vez, pero con esa esencia suya tan bacana.
        """
    elif promedio_general >= 3:
        mensaje = """
        Vamos bien, vamos bien.  
        Usted ya está viendo esas cositas que puede pulir, y eso es lo importante.  
        Su capacidad de análisis es su superpoder, pero no se me encierre mucho en los detalles.  
        Esta semana, escoja una de esas áreas y trabajela con calma, sin afán. ¡Usted puede!
        """
    else:
        mensaje = """
        Ay, no se me agüeve.  
        Estas semanas de aprendizaje son las que más nos dejan.  
        Reconocer que hay desafíos ya es un montón.  
        Usted tiene una base sólida, así que tómelo con calma, analice qué pasó y para la próxima semana hacemos un ajustecito.  
        Todo es parte del proceso, ¿cierto?
        """
    
    # Mostrar reflexión con HTML
    st.markdown(f"""
    <div style="
        background: #ffffff;
        border-radius: 16px;
        padding: 24px 32px 20px 32px;
        margin: 16px 0 24px 0;
        border: 1px solid #e9edf2;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    ">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <span style="font-size: 28px;">💡</span>
            <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 600;">Reflexión de la semana</h3>
        </div>
        <div style="font-size: 17px; line-height: 1.8; color: #1e293b; padding: 0 4px;">
            {mensaje.replace(chr(10), '<br>')}
        </div>
        <div style="
            margin-top: 18px;
            padding-top: 14px;
            border-top: 2px solid #f1f5f9;
            font-size: 15px;
            color: #64748b;
            font-style: italic;
            padding-left: 4px;
        ">
            “Mi objetivo no es cambiar quién soy, sino utilizar conscientemente mis fortalezas y desarrollar las capacidades que las complementan.”
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- SECCIÓN 2: RESUMEN DE PROGRESO ---
    st.markdown("## 🎯 Resumen de tu progreso")
    
    mejor_indicador = max(promedios, key=promedios.get)
    peor_indicador = min(promedios, key=promedios.get)
    
    nombres_indicadores = {
        'analysis': 'Análisis',
        'flexibility': 'Flexibilidad',
        'delegation': 'Delegación',
        'communication': 'Comunicación',
        'development': 'Desarrollo',
        'serenity': 'Serenidad',
        'balance': 'Balance'
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📅 Semanas",
            value=total_semanas,
            delta="¡Sigue así!" if total_semanas > 0 else None
        )
    
    with col2:
        st.metric(
            label="⭐ Promedio",
            value=f"{promedio_general:.1f}/5",
            delta="Buen camino" if promedio_general >= 3.5 else "Área de mejora"
        )
    
    with col3:
        st.metric(
            label="💪 Mayor fortaleza",
            value=nombres_indicadores.get(mejor_indicador, mejor_indicador),
            delta=f"{promedios[mejor_indicador]:.1f}/5"
        )
    
    with col4:
        st.metric(
            label="🎯 Área de mejora",
            value=nombres_indicadores.get(peor_indicador, peor_indicador),
            delta=f"{promedios[peor_indicador]:.1f}/5"
        )
    
    st.markdown("---")
    
    # --- SECCIÓN 3: EVOLUCIÓN (GRÁFICO NATIVO DE STREAMLIT) ---
    st.markdown("## 📈 Evolución de tus indicadores")
    
    # Obtener los últimos registros para el gráfico
    records = db.query(WeeklyRecord).filter(
        WeeklyRecord.user_id == user_id
    ).order_by(WeeklyRecord.date.asc()).all()
    
    if len(records) > 1:
        # Preparar datos para el gráfico de líneas
        semanas = [r.week_number for r in records]
        datos = {
            "Análisis": [r.analysis_score for r in records],
            "Flexibilidad": [r.flexibility_score for r in records],
            "Delegación": [r.delegation_score for r in records],
            "Comunicación": [r.communication_score for r in records],
            "Desarrollo": [r.development_score for r in records],
            "Serenidad": [r.serenity_score for r in records],
            "Balance": [r.balance_score for r in records]
        }
        
        # Convertir a formato para st.line_chart
        import pandas as pd
        # (pandas solo se usa aquí, pero si falla, podemos hacerlo con listas)
        # Usamos un DataFrame solo para este gráfico
        df = pd.DataFrame(datos, index=semanas)
        st.line_chart(df)
        
        st.caption("Evolución de tus indicadores semana a semana.")
    else:
        st.info("📊 Necesitas al menos 2 semanas de registros para ver tu evolución.")
    
    st.markdown("---")
    
    # --- SECCIÓN 4: ESTADO ACTUAL (BARRAS HORIZONTALES) ---
    st.markdown("## 🎯 Estado actual de tus indicadores")
    
    ultimo = stats.get('latest')
    if ultimo:
        scores = {
            'Análisis': ultimo.analysis_score,
            'Flexibilidad': ultimo.flexibility_score,
            'Delegación': ultimo.delegation_score,
            'Comunicación': ultimo.communication_score,
            'Desarrollo': ultimo.development_score,
            'Serenidad': ultimo.serenity_score,
            'Balance': ultimo.balance_score
        }
        
        def get_color(valor):
            if valor >= 4:
                return '#10b981'
            elif valor >= 3:
                return '#f59e0b'
            else:
                return '#ef4444'
        
        for nombre, valor in scores.items():
            color = get_color(valor)
            porcentaje = (valor / 5) * 100
            emoji = "🌟" if valor >= 4 else "💪" if valor >= 3 else "🎯"
            
            st.markdown(f"""
            <div style="margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-weight: 500; font-size: 16px; color: #1e293b;">{emoji} {nombre}</span>
                    <span style="font-weight: 600; font-size: 16px; color: #1e293b;">{valor}/5</span>
                </div>
                <div style="width: 100%; background-color: #e2e8f0; border-radius: 10px; height: 24px; overflow: hidden;">
                    <div style="width: {porcentaje}%; background-color: {color}; height: 100%; border-radius: 10px; display: flex; align-items: center; justify-content: flex-end; padding-right: 10px; transition: width 0.5s;">
                        <span style="color: white; font-size: 12px; font-weight: 600;">{porcentaje:.0f}%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Botón para nuevo registro
    st.markdown("---")
    if st.button("📝 Registrar nueva semana", use_container_width=True):
        st.switch_page("app/pages/new_record.py")
