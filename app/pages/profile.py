import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def show_profile():
    # Verificar autenticación
    if not st.session_state.get('authenticated', False):
        st.warning("⚠️ Por favor inicia sesión")
        st.session_state.page = "main"
        st.rerun()
        return
    
    st.title("🧬 Mi Perfil Temperamental (CT)")
    st.caption(f"Basado en tu evaluación - {st.session_state.user['name']}")
    
    # --- ESTILO PORTADA DEL PDF (SIN GRÁFICOS) ---
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 20px;
        padding: 32px 40px;
        margin: 16px 0 24px 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        text-align: center;
    ">
        <p style="
            color: #475569; 
            font-size: 16px; 
            margin: 0 0 12px 0;
            font-weight: 400;
            letter-spacing: 0.5px;
        ">
            Compositum Temperamental (CT)
        </p>
        <h1 style="
            color: #0f172a; 
            font-size: 36px; 
            font-weight: 700; 
            margin: 0 0 8px 0;
            letter-spacing: -0.5px;
        ">
            Autístico <span style="color: #64748b; font-weight: 300;">—</span> Normaloide <span style="color: #64748b; font-weight: 300;">—</span> Epileptoide
        </h1>
        <div style="
            display: flex;
            justify-content: center;
            gap: 24px;
            margin-top: 8px;
            flex-wrap: wrap;
        ">
            <span style="
                background: #dbeafe;
                color: #1e40af;
                padding: 4px 16px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 500;
            ">🔵 Principal</span>
            <span style="
                background: #e0e7ff;
                color: #3730a3;
                padding: 4px 16px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 500;
            ">🟣 Modificador</span>
            <span style="
                background: #fef3c7;
                color: #92400e;
                padding: 4px 16px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 500;
            ">🟡 Matiz</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- FRASE INTRODUCTORIA (COMO EN EL PDF) ---
    st.markdown("""
    <div style="
        background: #ffffff;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 8px 0 24px 0;
        border-left: 4px solid #2563eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    ">
        <p style="
            color: #334155; 
            font-size: 15px; 
            line-height: 1.7; 
            margin: 0;
            font-style: italic;
        ">
            “Al igual que en el genoma humano, el Compositum Temperamental (CT) nos da información 
            de aquellos rasgos de comportamiento que hemos heredado al nacer y que nos determinan 
            a lo largo de la vida. La combinación y el nivel de intensidad con el que cada componente 
            está presente, nos hace seres únicos e irrepetibles.”
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- DESCRIPCIÓN DEL PERFIL (EN TARJETAS) ---
    st.markdown("## 📖 Tus perfiles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background: #ffffff;
            border-radius: 12px;
            padding: 16px 20px;
            border: 1px solid #e9edf2;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            margin-bottom: 16px;
            height: 100%;
        ">
            <h4 style="color: #2563eb; margin: 0 0 8px 0;">🧑 Perfil Personal</h4>
            <p style="color: #334155; font-size: 14px; line-height: 1.6; margin: 0;">
                Decisiones pensadas y ponderadas, con reflexión profunda del impacto en otros. 
                Puedes ser juzgado de lento por tu perfeccionismo. Te adaptas a urgencias aunque 
                las sufres internamente. Te sientes cómodo con normas y procesos establecidos.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: #ffffff;
            border-radius: 12px;
            padding: 16px 20px;
            border: 1px solid #e9edf2;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            margin-bottom: 16px;
            height: 100%;
        ">
            <h4 style="color: #2563eb; margin: 0 0 8px 0;">💼 Perfil Profesional</h4>
            <p style="color: #334155; font-size: 14px; line-height: 1.6; margin: 0;">
                Aptitud para la mejora, el detalle, el proceso y el orden. Eficaz reduciendo costos, 
                plazos o errores. Destacas en calidad, finanzas y retos que exigen normalizar 
                o vertebrar la organización. Más volcado a soluciones técnicas que humanas.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: #ffffff;
            border-radius: 12px;
            padding: 16px 20px;
            border: 1px solid #e9edf2;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            margin-bottom: 16px;
            height: 100%;
        ">
            <h4 style="color: #2563eb; margin: 0 0 8px 0;">👥 Perfil Social</h4>
            <p style="color: #334155; font-size: 14px; line-height: 1.6; margin: 0;">
                Te sientes cómodo en relaciones centradas en información técnica. Tu inclinación 
                natural es aportar soluciones. Destacas por tu capacidad de escucha, aunque puedes 
                parecer frío. Prefieres conversaciones racionales.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: #ffffff;
            border-radius: 12px;
            padding: 16px 20px;
            border: 1px solid #e9edf2;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            margin-bottom: 16px;
            height: 100%;
        ">
            <h4 style="color: #2563eb; margin: 0 0 8px 0;">📊 Perfil Directivo</h4>
            <p style="color: #334155; font-size: 14px; line-height: 1.6; margin: 0;">
                Llevas la iniciativa pero prefieres que el protagonismo recaiga sobre tu unidad. 
                Necesitas controlar de cerca normas y procesos. Tu liderazgo se centra en tu 
                conocimiento, experiencia y capacidad de asumir responsabilidades.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # --- TERCER COMPONENTE: EPILEPTOIDE ---
    st.markdown("## 🧩 Tu tercer componente: Epileptoide")
    st.markdown("""
    <div style="
        background: #fffbeb;
        border-radius: 12px;
        padding: 20px 24px;
        border: 1px solid #fde68a;
        margin: 8px 0 16px 0;
    ">
        <p style="color: #78350f; font-size: 15px; line-height: 1.8; margin: 0;">
            Tu tercer componente temperamental <strong>“E: Epileptoide”</strong> te facilita la atención al detalle 
            y el perfeccionismo, probablemente no en todos los ámbitos de tu vida, pero sí 
            específicamente en algunos donde puedes dedicar gran cantidad de tiempo sin que 
            te genere mucho esfuerzo.
        </p>
        <p style="color: #78350f; font-size: 15px; line-height: 1.8; margin-top: 12px;">
            Este componente es de gran aporte a los equipos, ya que impulsa la mejora continua 
            y el cuidado de los detalles. Sin embargo, ten cuidado ya que puedes en ocasiones 
            perder eficiencia al dedicar tiempo a mejoras innecesarias.
        </p>
        <p style="color: #78350f; font-size: 15px; line-height: 1.8; margin-top: 12px;">
            <strong>Aprovecha el potencial</strong> que te da este tercer componente, el cual te permite ser 
            cuidadoso con los detalles, las formas y la calidad que logras en lo que haces.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- PUNTOS CIEGOS ---
    st.markdown("## 🔍 Áreas de Atención (Puntos Ciegos)")
    st.caption("Fortalezas que pueden llevarse al extremo si no se equilibran conscientemente.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning("**🔸 Análisis → Sobreanálisis**\n\nPuedes quedarte atascado en la búsqueda de la solución perfecta, perdiendo eficiencia.")
        st.warning("**🔸 Calidad → Perfeccionismo**\n\nPuedes retrasar entregas por detalles que no impactan el resultado final.")
    
    with col2:
        st.warning("**🔸 Orden → Rigidez**\n\nTe cuesta adaptarte a cambios de última hora o a procesos no establecidos.")
        st.warning("**🔸 Responsabilidad → Cargar con todo**\n\nTiendes a no delegar porque 'nadie lo hará tan bien como tú'.")
    
    # --- FRASE GUÍA ---
    st.markdown("---")
    st.caption("💡 *'Mi objetivo no es cambiar quién soy, sino utilizar conscientemente mis fortalezas y desarrollar las capacidades que las complementan.'*")
    
    # --- BOTÓN PARA VOLVER ---
    if st.button("⬅️ Volver al Dashboard", use_container_width=True):
        st.switch_page("app/pages/dashboard.py")