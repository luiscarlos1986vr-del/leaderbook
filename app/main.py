import streamlit as st
import sys
import os

# Agregar la carpeta raíz al path para poder importar app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la función para crear tablas (se ejecutará al inicio)
from app.models.database import create_tables

# Configuración de la página
st.set_page_config(
    page_title="Digital Leader Book",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ CREAR TABLAS SI NO EXISTEN (¡Esto resuelve el error!)
try:
    create_tables()
except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    st.stop()

# Inicializar estado de sesión
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.page = "main"

def main():
    # Sidebar
    with st.sidebar:
        st.title("📋 Menú")
        st.markdown("---")
        
        if st.session_state.authenticated:
            st.write(f"👤 {st.session_state.user['name']}")
            st.markdown("---")
            if st.button("🚪 Cerrar Sesión", use_container_width=True, key="logout_btn"):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.page = "main"
                st.rerun()
        else:
            if st.button("🔐 Iniciar Sesión", use_container_width=True, key="login_sidebar"):
                st.session_state.page = "login"
                st.rerun()
            if st.button("📝 Registrarse", use_container_width=True, key="register_sidebar"):
                st.session_state.page = "register"
                st.rerun()
        
        st.markdown("---")
        st.caption("v1.0.0")
    
    # Navegación de páginas
    if st.session_state.authenticated:
        nav_page = st.sidebar.radio(
            "Navegación",
            ["Dashboard", "Nuevo Registro", "Historial", "Perfil CT", "Retroalimentación IA"],
            key="nav_radio"
        )
        
        if nav_page == "Dashboard":
            from app.pages.dashboard import show_dashboard
            show_dashboard()
        elif nav_page == "Nuevo Registro":
            from app.pages.new_record import show_new_record
            show_new_record()
        elif nav_page == "Historial":
            from app.pages.history import show_history
            show_history()
        elif nav_page == "Perfil CT":
            from app.pages.profile import show_profile
            show_profile()
        elif nav_page == "Retroalimentación IA":
            from app.pages.ai_feedback import show_ai_feedback
            show_ai_feedback()
    else:
        if st.session_state.page == "login":
            from app.pages.login import show_login
            show_login()
        elif st.session_state.page == "register":
            from app.pages.register import show_register
            show_register()
        else:
            st.title("🚀 Digital Leader Book")
            st.write("¡Bienvenido a tu herramienta de desarrollo personal!")
            st.info("🔐 Por favor inicia sesión o regístrate para continuar")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔐 Iniciar Sesión", use_container_width=True, key="login_main"):
                    st.session_state.page = "login"
                    st.rerun()
            with col2:
                if st.button("📝 Registrarse", use_container_width=True, key="register_main"):
                    st.session_state.page = "register"
                    st.rerun()

if __name__ == "__main__":
    main()
