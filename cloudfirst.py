import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
from datetime import datetime

# --- Configuración de la Página ---
st.set_page_config(page_title="Sistema de Evaluación de Riesgo", page_icon="💼", layout="centered")

# --- Configuración de Gemini (Google AI) ---
# Intentamos obtener la clave de las variables de entorno (Nube)
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    # Opción para pruebas locales si no has configurado variables de entorno
    # NO subas esto a GitHub, es solo para que te funcione en tu PC ahora mismo si quieres
    # st.warning("⚠️ API Key no encontrada en variables de entorno.")
    pass

def generar_explicacion_agentic(nombre, decision, riesgo, dti):
    """Consulta real a Gemini para generar feedback."""
    if not api_key:
        return "⚠️ La IA no está activa (Falta API Key). Se muestra resultado estándar."
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Actúa como un analista de riesgos senior. Escribe un veredicto de 1 párrafo para {nombre}.
        Datos: Decisión={decision}, Riesgo={riesgo}, DTI={dti:.1%}.
        Tono: Corporativo y directo. Si es rechazado, explica por qué sin pedir disculpas.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error de conexión con IA: {str(e)}"

# --- Estilos CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #003366; color: white; border-radius: 5px; }
    .result-box { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-top: 5px solid #ccc; margin-top: 20px;}
    </style>
    """, unsafe_allow_html=True)

st.title("💼 Sistema de Evaluación Híbrido")
st.markdown("### AWS (Motor) + GCP (Cerebro)")

# --- Formulario ---
with st.form("evaluador_form"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del Cliente", value="Empresa Demo")
        ingreso = st.number_input("Ingreso Mensual ($)", value=50000.0)
        deudas = st.number_input("Deudas Actuales ($)", value=15000.0)
    with col2:
        monto = st.number_input("Monto Solicitado ($)", value=200000.0)
        plazo = st.number_input("Plazo (meses)", value=36)
        score = st.slider("Score Crediticio", 0, 100, 85)

    boton_evaluar = st.form_submit_button("Ejecutar Análisis")

# --- Lógica ---
if boton_evaluar:
    cuota = (monto / plazo) * 1.1
    dti = (deudas + cuota) / ingreso
    
    # Reglas simples para el demo
    if dti > 0.5 or score < 60:
        decision = "Rechazado"
        riesgo = "Alto"
        color = "#c62828" # Rojo
    else:
        decision = "Aprobado"
        riesgo = "Bajo"
        color = "#2e7d32" # Verde

    # --- LLAMADA A LA IA (GCP) ---
    with st.spinner('Consultando a Gemini en Google Cloud...'):
        explicacion = generar_explicacion_agentic(nombre, decision, riesgo, dti)

    # --- Resultado ---
    st.markdown(f"""
        <div class="result-box" style="border-top-color: {color};">
            <h3 style="color: {color};">{decision}</h3>
            <p><b>Riesgo:</b> {riesgo} | <b>DTI:</b> {dti:.1%}</p>
            <hr>
            <p><i>🤖 Análisis de IA:</i> {explicacion}</p>
        </div>
    """, unsafe_allow_html=True)