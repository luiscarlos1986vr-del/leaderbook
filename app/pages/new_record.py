import streamlit as st
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import get_db
from app.services.record_service import create_record

def show_new_record():
    # Verificar autenticación
    if not st.session_state.get('authenticated', False):
        st.warning("⚠️ Por favor inicia sesión")
        st.session_state.page = "main"
        st.rerun()
        return
    
    st.title("📝 Registro Semanal - CT")
    st.caption(f"Semana {get_week_number()} - {st.session_state.user['name']}")
    
    # Mostrar recordatorio del perfil CT con ejemplos
    with st.expander("🧬 Mi Perfil CT: Autístico-Normaloide con matiz Epileptoide", expanded=True):
        st.markdown("""
        **🎯 Tus superpoderes naturales:**
        - ✅ **Análisis profundo:** Ves patrones y conexiones que otros no ven
        - ✅ **Atención al detalle:** Encuentras errores y oportunidades de mejora
        - ✅ **Estructura y orden:** Organizas proyectos complejos con facilidad
        - ✅ **Responsabilidad:** Cumples y generas confianza en tu equipo
        
        **⚠️ Tus áreas de crecimiento (puntos ciegos):**
        - 🔸 **Análisis → Sobreanálisis:** Pasas demasiado tiempo buscando la "solución perfecta"
        - 🔸 **Calidad → Perfeccionismo:** Retrasas entregas por detalles que no impactan el resultado
        - 🔸 **Orden → Rigidez:** Te cuesta adaptarte a cambios de última hora
        - 🔸 **Responsabilidad → Cargar con todo:** No delegas porque "nadie lo hará tan bien como tú"
        """)
    
    st.markdown("---")
    
    with st.form("weekly_record_form"):
        st.markdown("### 1. Conocer mi potencial")
        st.caption("💡 **Ejemplo:** *'Esta semana usé mi capacidad de análisis para identificar un error en el cálculo de IVA que nadie había visto. Esto ayudó a mi jefe a tomar una decisión clave y responder a la auditoría.'*")
        
        col1, col2 = st.columns(2)
        with col1:
            potential_personal = st.text_area(
                "Personal: ¿Qué hice naturalmente bien?",
                placeholder="Ejemplo: Usé mi capacidad de escucha para entender el problema de mi pareja sin juzgar, y mi análisis ayudó a ver la situación desde otra perspectiva.",
                height=100
            )
        with col2:
            potential_professional = st.text_area(
                "Profesional: ¿Qué valor aporté a mi equipo?",
                placeholder="Ejemplo: Mi atención al detalle me permitió encontrar un error en una conciliación bancaria que evitó un problema financiero. Aporté orden a un proceso desorganizado.",
                height=100
            )
        
        evidence = st.text_area(
            "📌 Evidencia concreta de esta semana:",
            placeholder="Ejemplo: El martes, mientras revisaba los estados de cuenta, noté una discrepancia de $5,000 que resultó ser un error del proveedor. Mi jefe pudo reclamar a tiempo.",
            height=80
        )
        
        st.markdown("### 2. Identificar mis puntos ciegos")
        st.caption("💡 **Ejemplo:** *'Me tomó 3 horas adicionales perfeccionando un informe que ya estaba bien, solo para ganar un 2% de mejora. Esto retrasó la reunión con el cliente.'*")
        
        col1, col2 = st.columns(2)
        with col1:
            blindspot_personal = st.text_area(
                "Personal: ¿Qué observé en mi vida personal?",
                placeholder="Ejemplo: En una discusión con mi pareja, me enfoqué tanto en 'resolver el problema' lógicamente que no validé sus emociones. Se sintió no escuchada.",
                height=100
            )
        with col2:
            blindspot_professional = st.text_area(
                "Profesional: ¿Qué observé en mi trabajo?",
                placeholder="Ejemplo: Pasé 4 horas perfeccionando un PowerPoint que ya estaba bien. Mi perfeccionismo retrasó la entrega y el equipo tuvo que trabajar horas extra.",
                height=100
            )
        
        st.markdown("**🔍 ¿Cuáles de estos puntos ciegos identificaste esta semana?**")
        col1, col2 = st.columns(2)
        with col1:
            c1 = st.checkbox("🔸 Análisis → Sobreanálisis (me quedé atascado en detalles)")
            c2 = st.checkbox("🔸 Calidad → Perfeccionismo (retrasé algo por buscar la perfección)")
        with col2:
            c3 = st.checkbox("🔸 Orden → Rigidez (me costó adaptarme a un cambio inesperado)")
            c4 = st.checkbox("🔸 Responsabilidad → Cargar con todo (no delegué algo que debía delegar)")
        
        st.markdown("### 3. Adaptar mi liderazgo")
        st.caption("💡 **Ejemplo:** *'En lugar de dar la solución inmediata, pregunté a mi equipo: ¿Qué opciones ven ustedes? Esperé 5 minutos antes de intervenir.'*")
        
        col1, col2 = st.columns(2)
        with col1:
            adaptation_personal = st.text_area(
                "Personal: ¿Escuché antes de resolver?",
                placeholder="Ejemplo: Cuando mi pareja me contó su problema, en lugar de darle soluciones, le pregunté: '¿Cómo te sientes al respecto?' y solo escuché durante 10 minutos.",
                height=80
            )
        with col2:
            adaptation_professional = st.text_area(
                "Profesional: ¿Cómo desarrollé a mi equipo?",
                placeholder="Ejemplo: En lugar de hacer yo el análisis complejo, se lo asigné a un junior, le di las herramientas y lo dejé equivocarse. Aprendió más que si yo lo hubiera hecho.",
                height=80
            )
        
        communication = st.text_area(
            "🗣️ ¿Comuniqué con claridad y respeto?",
            placeholder="Ejemplo: En la reunión, en lugar de usar jerga técnica, expliqué el problema con un ejemplo simple que todos entendieron. Pregunté: '¿Hay dudas?' y esperé.",
            height=80
        )
        
        st.markdown("### 4. Diseñar hábitos para la próxima semana")
        st.caption("💡 **Ejemplo:** *'En mis próximas 3 reuniones, me forzaré a preguntar ¿Cómo te sientes con este plan? antes de dar mi opinión.'*")
        
        habit_strength = st.text_input(
            "💪 Una fortaleza que aprovecharé",
            placeholder="Ejemplo: Usaré mi capacidad de análisis para identificar los 3 riesgos clave del proyecto, pero pondré un límite de 30 minutos de análisis."
        )
        
        habit_challenge = st.text_input(
            "🎯 Un desafío que debo trabajar",
            placeholder="Ejemplo: Mi dificultad para delegar. Esta semana delegaré al menos una tarea compleja a un miembro del equipo."
        )
        
        habit_practice = st.text_input(
            "📅 Un hábito que practicaré",
            placeholder="Ejemplo: Antes de dar una solución en casa o en el trabajo, haré 3 preguntas para entender la perspectiva de la otra persona."
        )
        
        st.markdown("### 5. Auto-evaluación (1-5)")
        st.caption("Basado en tu perfil CT, evalúa cómo manejaste tus fortalezas y puntos ciegos esta semana")
        
        col1, col2 = st.columns(2)
        
        with col1:
            analysis_score = st.slider("🧠 Análisis equilibrado", 1, 5, 3, 1,
                                       help="¿Lograste analizar sin caer en sobreanálisis?")
            flexibility_score = st.slider("🔄 Flexibilidad", 1, 5, 3, 1,
                                         help="¿Te adaptaste bien a cambios o imprevistos?")
            delegation_score = st.slider("🤝 Delegación", 1, 5, 3, 1,
                                         help="¿Confiaste y asignaste tareas a otros?")
        with col2:
            communication_score = st.slider("💬 Comunicación", 1, 5, 3, 1,
                                            help="¿Te comunicaste con claridad y empatía?")
            development_score = st.slider("🌱 Desarrollo de personas", 1, 5, 3, 1,
                                          help="¿Ayudaste a crecer a otros?")
            serenity_score = st.slider("🧘 Serenidad ante incertidumbre", 1, 5, 3, 1,
                                       help="¿Mantuviste la calma ante lo inesperado?")
        
        balance_score = st.slider("⚖️ Balance Personal-Profesional", 1, 5, 3, 1,
                                   help="¿Cómo fue tu equilibrio entre vida personal y profesional esta semana?")
        
        # Frase guía
        st.markdown("---")
        st.caption("💡 *'Mi objetivo no es cambiar quién soy, sino utilizar conscientemente mis fortalezas y desarrollar las capacidades que las complementan.'*")
        st.caption("— Luis Carlos Valencia (Autístico-Normaloide con matiz Epileptoide)")
        
        submitted = st.form_submit_button("Guardar Registro", use_container_width=True)
        
        if submitted:
            # Validar campos requeridos
            required_fields = [
                potential_personal, potential_professional,
                blindspot_personal, blindspot_professional,
                adaptation_personal, adaptation_professional,
                habit_strength, habit_challenge, habit_practice
            ]
            
            if not all(required_fields):
                st.error("❌ Por favor completa todos los campos")
                return
            
            # Construir datos
            record_data = {
                'potential_personal': potential_personal,
                'potential_professional': potential_professional,
                'blindspot_personal': blindspot_personal,
                'blindspot_professional': blindspot_professional,
                'adaptation_personal': adaptation_personal,
                'adaptation_professional': adaptation_professional,
                'habit_strength': habit_strength,
                'habit_challenge': habit_challenge,
                'habit_practice': habit_practice,
                'analysis_score': analysis_score,
                'flexibility_score': flexibility_score,
                'delegation_score': delegation_score,
                'communication_score': communication_score,
                'development_score': development_score,
                'serenity_score': serenity_score,
                'balance_score': balance_score
            }
            
            # Guardar campos extra
            record_data['evidence'] = evidence
            record_data['blindspots'] = {
                'sobreanalisis': c1,
                'perfeccionismo': c2,
                'rigidez': c3,
                'responsabilidad': c4
            }
            record_data['communication'] = communication
            
            try:
                db = next(get_db())
                # Importar record_service aquí para evitar dependencia circular
                from app.services.record_service import create_record as save_record
                record = save_record(db, st.session_state.user['id'], record_data)
                st.success(f"✅ ¡Registro de la semana {record.week_number} guardado exitosamente!")
                st.balloons()
            except ValueError as e:
                st.error(f"❌ {str(e)}")
            except Exception as e:
                st.error(f"❌ Error al guardar: {str(e)}")

def get_week_number():
    """Calcula el número de semana actual"""
    now = datetime.now()
    start_date = datetime(now.year, 1, 1)
    days = (now - start_date).days
    return (days + start_date.weekday() + 1) // 7 + 1