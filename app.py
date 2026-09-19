import streamlit as st
import pyodbc
from datetime import datetime

# --- 1. Función para conectar a la base de datos ---
# @st.cache_resource hace que la conexión se cree una sola vez y sea más rápida.
@st.cache_resource
def init_connection():
    # Construye la cadena de conexión usando los secretos de Streamlit
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={st.secrets['server']};"
        f"DATABASE={st.secrets['database']};"
        f"UID={st.secrets['username']};"
        f"PWD={st.secrets['password']};"
        "TrustServerCertificate=yes;"  # Necesario para conexiones a Somee
    )
    return pyodbc.connect(conn_str)

# --- 2. Función para insertar los datos en la tabla ---
def insertar_registro(nombre, fecha, hora):
    conn = init_connection()
    cursor = conn.cursor()
    
    # ⚠️ IMPORTANTE: Revisa que los nombres de las columnas (Nombre, Fecha, Hora)
    # coincidan EXACTAMENTE con los de tu tabla dbo.Super_Christian
    query = "INSERT INTO dbo.Super_Christian (Nombre, Fecha, Hora) VALUES (?, ?, ?)"
    
    cursor.execute(query, (nombre, fecha, hora))
    conn.commit()
    cursor.close()

# --- 3. Interfaz de Streamlit ---
st.title("📋 Registro de Datos - Super Christian")
st.write("Completa el formulario para añadir un nuevo registro a la base de datos.")

# Usamos un formulario para agrupar los campos
with st.form("registro_form", clear_on_submit=True):
    nombre = st.text_input("Nombre")
    fecha = st.date_input("Fecha")
    hora = st.time_input("Hora")
    
    # Botón de envío
    submitted = st.form_submit_button("Guardar Registro")

    if submitted:
        if nombre:  # Validación básica
            try:
                insertar_registro(nombre, fecha, hora)
                st.success(f"✅ Registro de '{nombre}' guardado exitosamente.")
            except Exception as e:
                st.error(f"❌ Error al guardar: {e}")
        else:
            st.warning("⚠️ El campo 'Nombre' es obligatorio.")