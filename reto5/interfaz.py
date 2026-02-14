import streamlit as st

# --- Configuración de la Página (Look Profesional) ---
st.set_page_config(
    page_title="Sistema de Evaluación de Riesgo",
    page_icon="💼",
    layout="centered"
)

# --- CSS Corporativo Personalizado ---
# Cambiamos los fondos pastel por bordes sólidos y sombras sutiles
st.markdown("""
    <style>
    /* Fondo general gris muy claro para contraste */
    .main { background-color: #f8f9fa; }

    /* Botón principal azul marino corporativo */
    .stButton>button {
        width: 100%;
        background-color: #003366;
        color: white;
        font-weight: 600;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover { background-color: #004080; }

    /* Caja de Resultado Corporativa: Fondo blanco, sombra y borde superior */
    .result-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 8px;
        margin-top: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); /* Sombra sutil elegante */
        border-top: 6px solid #ccc; /* Borde por defecto (gris) */
    }
    .result-header {
        margin-top: 0;
        font-weight: 700;
    }
    .metric-label { font-size: 0.9em; color: #666; }
    .metric-value { font-size: 1.1em; font-weight: bold; color: #333; }
    hr { margin: 15px 0; border-top: 1px solid #eee;}
    </style>
    """, unsafe_allow_html=True)

st.title("💼 Sistema de Evaluación de Crédito")
st.markdown("### Panel de Análisis de Riesgo")
st.write("Ingrese los datos del solicitante para ejecutar el motor de decisión.")
st.write("---")

# --- Formulario de Entrada (Igual que antes) ---
with st.form("evaluador_form"):
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre del Cliente", value="Ejemplo Corporativo")
        edad = st.number_input("Edad (años)", min_value=18, max_value=80, value=30)
        ingreso = st.number_input("Ingreso Mensual Neto ($)", min_value=0.0, step=1000.0, value=50000.0)
        deudas = st.number_input("Pago Mensual Deudas Actuales ($)", min_value=0.0, value=10000.0)

    with col2:
        monto = st.number_input("Monto de Crédito Solicitado ($)", min_value=0.0, step=5000.0, value=200000.0)
        plazo = st.number_input("Plazo en meses", min_value=12, max_value=72, value=36)
        # Ajusté el valor default a 85 para que veas el "verde" fácilmente
        score = st.slider("Puntaje Crediticio Interno (Score)", 0, 100, 85)
        atrasos = st.number_input("Pagos atrasados (último año)", min_value=0, max_value=12, value=0)

    st.markdown("**Garantías Adicionales**")
    tiene_aval = st.radio("¿Cuenta con aval calificado o garantía real?", ("No", "Sí"), horizontal=True)

    boton_evaluar = st.form_submit_button("Ejecutar Análisis de Riesgo")

# --- Lógica del Algoritmo ---
if boton_evaluar:
    # Cálculos
    cuota_aprox = (monto / plazo) * 1.1
    proporcion_deuda = (deudas + cuota_aprox) / ingreso

    decision = ""
    riesgo = ""
    monto_final = 0

    # Variables para el estilo corporativo
    border_color = ""
    text_color = ""
    icon_status = ""

    # Colores Profesionales (Hex codes sólidos)
    COLOR_ROJO_CORP = "#c62828"   # Rojo oscuro profesional
    COLOR_VERDE_CORP = "#2e7d32"  # Verde bosque profesional
    COLOR_AMBAR_CORP = "#f57c00"  # Naranja oscuro para advertencia

    # REGLAS DE NEGOCIO
    if edad < 21 or edad > 70 or score < 50 or atrasos > 3 or proporcion_deuda > 0.6:
        # Excepción por Aval
        if 45 <= score <= 49 and tiene_aval == "Sí" and proporcion_deuda <= 0.35:
            decision = "Aprobado con Condiciones (Aval)"
            riesgo = "Medio"
            monto_final = monto * 0.7
            border_color = COLOR_AMBAR_CORP
            text_color = COLOR_AMBAR_CORP
            icon_status = "⚠️"
        else:
            decision = "Solicitud Rechazada por Riesgo"
            riesgo = "Alto"
            monto_final = 0
            border_color = COLOR_ROJO_CORP
            text_color = COLOR_ROJO_CORP
            icon_status = "⛔"

    elif proporcion_deuda <= 0.35 and score >= 80 and atrasos <= 1:
        decision = "Aprobación Total (Tasa Preferencial)"
        riesgo = "Bajo"
        monto_final = monto
        border_color = COLOR_VERDE_CORP
        text_color = COLOR_VERDE_CORP
        icon_status = "✅"

    elif score >= 60 and 0.35 < proporcion_deuda <= 0.5:
        monto_reducido = monto * 0.7
        nueva_cuota = (monto_reducido / plazo) * 1.1
        nueva_prop = (deudas + nueva_cuota) / ingreso

        if nueva_prop <= 0.4:
            decision = "Aprobación Ajustada por Capacidad"
            riesgo = "Medio"
            monto_final = monto_reducido
            border_color = COLOR_AMBAR_CORP
            text_color = COLOR_AMBAR_CORP
            icon_status = "⚠️"
        else:
            decision = "Rechazado (DTI Excedido tras ajuste)"
            riesgo = "Alto"
            monto_final = 0
            border_color = COLOR_ROJO_CORP
            text_color = COLOR_ROJO_CORP
            icon_status = "⛔"
    else:
        decision = "Rechazado (Criterios no cubiertos)"
        riesgo = "Alto"
        monto_final = 0
        border_color = COLOR_ROJO_CORP
        text_color = COLOR_ROJO_CORP
        icon_status = "⛔"

    # --- Salida Visual Corporativa (Sin Pasteles, Sin Globos) ---

    # 1. Notificación Profesional (Toast) en lugar de globos
    if riesgo == "Bajo":
        st.toast("Análisis completado: Perfil de bajo riesgo detectado.", icon="✅")
        st.success("Operación Exitosa: El cliente califica para la oferta máxima.")
    elif riesgo == "Medio":
         st.toast("Análisis completado: Se requiere ajuste en la oferta.", icon="⚠️")
    else:
         st.toast("Análisis completado: No viable bajo políticas actuales.", icon="⛔")


    # 2. Caja de Resultados Estilo Dashboard Ejecutivo
    # Usamos 'border-top-color' para la barra de color superior
    st.markdown(f"""
        <div class="result-box" style="border-top-color: {border_color};">
            <h3 class="result-header" style="color: {text_color};">
                {icon_status} {decision}
            </h3>
            <hr>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <p class="metric-label">Solicitante</p>
                    <p class="metric-value">{nombre}</p>
                </div>
                <div>
                    <p class="metric-label">Nivel de Riesgo Calculado</p>
                    <p class="metric-value" style="color: {text_color};">{riesgo.upper()}</p>
                </div>
                <div>
                    <p class="metric-label">Capacidad de Pago (DTI)</p>
                    <p class="metric-value">{proporcion_deuda:.1%}</p>
                </div>
                <div>
                    <p class="metric-label">Monto Final Autorizado</p>
                    <p class="metric-value" style="font-size: 1.3em; color: #003366;">
                        ${monto_final:,.2f}
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)