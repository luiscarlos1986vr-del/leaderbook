# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 16:42:55 2026

@author: user1
"""

import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import get_db
from app.models.database import WeeklyRecord

def show_history():
    # Verificar autenticación
    if not st.session_state.get('authenticated', False):
        st.warning("⚠️ Por favor inicia sesión")
        st.session_state.page = "main"
        st.rerun()
        return
    
    st.title("📚 Historial de Registros")
    st.caption(f"Todos tus registros - {st.session_state.user['name']}")
    
    db = next(get_db())
    user_id = st.session_state.user['id']
    
    # Obtener todos los registros del usuario
    records = db.query(WeeklyRecord).filter(
        WeeklyRecord.user_id == user_id
    ).order_by(WeeklyRecord.date.desc()).all()
    
    if not records:
        st.info("📝 Aún no tienes registros. ¡Comienza tu primera semana de crecimiento!")
        if st.button("📝 Ir a Nuevo Registro", use_container_width=True):
            st.switch_page("app/pages/new_record.py")
        return
    
    # Mostrar resumen
    st.markdown(f"**Total de semanas registradas:** {len(records)}")
    
    # Preparar datos para la tabla
    data = []
    for r in records:
        data.append({
            "Semana": r.week_number,
            "Fecha": r.date.strftime("%d/%m/%Y"),
            "Análisis": r.analysis_score,
            "Flexibilidad": r.flexibility_score,
            "Delegación": r.delegation_score,
            "Comunicación": r.communication_score,
            "Desarrollo": r.development_score,
            "Serenidad": r.serenity_score,
            "Balance": r.balance_score,
            "Promedio": round((r.analysis_score + r.flexibility_score + r.delegation_score + 
                              r.communication_score + r.development_score + r.serenity_score + 
                              r.balance_score) / 7, 1),
            "id": r.id
        })
    
    df = pd.DataFrame(data)
    
    # Selector de filtro por semana
    semanas = sorted(df["Semana"].unique(), reverse=True)
    semana_seleccionada = st.selectbox("Filtrar por semana", ["Todas"] + [f"Semana {s}" for s in semanas])
    
    if semana_seleccionada != "Todas":
        semana_num = int(semana_seleccionada.split(" ")[1])
        df_filtrado = df[df["Semana"] == semana_num]
    else:
        df_filtrado = df
    
    # Mostrar tabla
    st.markdown("### 📊 Resumen por semana")
    
    # Columnas a mostrar (sin el id)
    columnas_mostrar = ["Semana", "Fecha", "Promedio", "Análisis", "Flexibilidad", "Delegación", 
                       "Comunicación", "Desarrollo", "Serenidad", "Balance"]
    
    st.dataframe(
        df_filtrado[columnas_mostrar].style.background_gradient(cmap="RdYlGn", subset=["Promedio"]),
        use_container_width=True,
        hide_index=True
    )
    
    # Detalle de un registro seleccionado
    st.markdown("---")
    st.markdown("### 📝 Ver detalle de un registro")
    
    if not df_filtrado.empty:
        semanas_disponibles = df_filtrado["Semana"].tolist()
        semana_detalle = st.selectbox("Selecciona una semana para ver el detalle", semanas_disponibles, key="detalle_semana")
        
        if semana_detalle:
            record = db.query(WeeklyRecord).filter(
                WeeklyRecord.user_id == user_id,
                WeeklyRecord.week_number == semana_detalle
            ).first()
            
            if record:
                with st.expander(f"📋 Detalle de la semana {record.week_number}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**🌱 Potencial Personal:**")
                        st.write(record.potential_personal)
                        st.markdown("**💼 Potencial Profesional:**")
                        st.write(record.potential_professional)
                        st.markdown("**🔍 Puntos Ciegos (Personal):**")
                        st.write(record.blindspot_personal)
                        st.markdown("**🔍 Puntos Ciegos (Profesional):**")
                        st.write(record.blindspot_professional)
                    
                    with col2:
                        st.markdown("**💡 Adaptación Personal:**")
                        st.write(record.adaptation_personal)
                        st.markdown("**💡 Adaptación Profesional:**")
                        st.write(record.adaptation_professional)
                        st.markdown("**💪 Hábitos:**")
                        st.write(f"Fortaleza: {record.habit_strength}")
                        st.write(f"Desafío: {record.habit_challenge}")
                        st.write(f"Práctica: {record.habit_practice}")
                    
                    # Mostrar feedback IA si existe
                    if record.ai_feedback and "Error" not in record.ai_feedback:
                        st.markdown("---")
                        st.markdown("**🤖 Retroalimentación IA (de esa semana):**")
                        st.markdown(record.ai_feedback)
    else:
        st.info("No hay registros para mostrar con el filtro seleccionado.")
    
    # Botón para volver al dashboard
    st.markdown("---")
    if st.button("⬅️ Volver al Dashboard", use_container_width=True):
        st.switch_page("app/pages/dashboard.py")