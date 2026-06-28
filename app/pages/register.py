import streamlit as st
import sys
import os

# Agregar la carpeta raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import get_db
from app.utils.auth import create_user

def show_register():
    st.title("📝 Registro de Usuario")
    
    if st.session_state.get('authenticated', False):
        st.session_state.page = "main"
        st.rerun()
        return
    
    # Variable para controlar si el registro fue exitoso
    registro_exitoso = False
    
    with st.form("register_form"):
        name = st.text_input("Nombre completo", key="register_name")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Contraseña", type="password", key="register_password")
        confirm_password = st.text_input("Confirmar contraseña", type="password", key="register_confirm")
        submitted = st.form_submit_button("Registrarse")
        
        if submitted:
            if not name or not email or not password:
                st.error("⚠️ Por favor completa todos los campos")
            elif password != confirm_password:
                st.error("❌ Las contraseñas no coinciden")
            elif len(password) < 6:
                st.error("❌ La contraseña debe tener al menos 6 caracteres")
            else:
                db = next(get_db())
                user, error = create_user(db, email, name, password)
                
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.success(f"✅ ¡Usuario {name} creado exitosamente!")
                    registro_exitoso = True
    
    # Botón fuera del formulario (después de cerrar el with)
    if registro_exitoso:
        st.info("🔐 Ahora puedes iniciar sesión")
        if st.button("🔐 Iniciar Sesión ahora", key="login_now"):
            st.session_state.page = "login"
            st.rerun()
    
    st.markdown("---")
    if st.button("🔐 ¿Ya tienes cuenta? Inicia sesión aquí", key="go_to_login"):
        st.session_state.page = "login"
        st.rerun()