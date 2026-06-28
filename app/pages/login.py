import streamlit as st
import sys
import os

# Agregar la carpeta raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import get_db
from app.utils.auth import authenticate_user

def show_login():
    st.title("🔐 Iniciar Sesión")
    
    if st.session_state.get('authenticated', False):
        st.session_state.page = "main"
        st.rerun()
        return
    
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Contraseña", type="password", key="login_password")
        submitted = st.form_submit_button("Iniciar Sesión")
        
        if submitted:
            if not email or not password:
                st.error("⚠️ Por favor completa todos los campos")
                return
            
            db = next(get_db())
            user, error = authenticate_user(db, email, password)
            
            if error:
                st.error(f"❌ {error}")
            else:
                st.session_state.authenticated = True
                st.session_state.user = {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name
                }
                st.session_state.page = "main"
                st.success(f"✅ ¡Bienvenido {user.name}!")
                st.rerun()
    
    st.markdown("---")
    if st.button("📝 Regístrate aquí"):
        st.session_state.page = "register"
        st.rerun()