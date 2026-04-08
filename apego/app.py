import streamlit as st
from fpdf import FPDF
from streamlit_lottie import st_lottie
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PBI Honduras - Psicología", page_icon="🧠", layout="wide")

def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# Animaciones dinámicas
ANIMACIONES = {
    "Óptimo": "https://lottie.host",
    "Cariñoso": "https://lottie.host", # Ejemplo
    "Crítico": "https://lottie.host"
}

# Estilo visual para evitar distorsiones
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    .header-pnh {
        background-color: #002244; color: white !important;
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 30px;
    }
    .resultado-card {
        padding: 20px; border-radius: 15px; border-left: 10px solid #003366;
        background-color: #f0f4f8; color: black; margin-bottom: 20px;
    }
    label, p, span { color: black !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("""
    <div class="header-pnh">
        <img src="https://wikimedia.org" width="80">
        <h1>POLICÍA NACIONAL DE HONDURAS</h1>
        <p>Unidad de Psicología | Evaluación de Vínculo Parental (PBI)</p>
    </div>
    """, unsafe_allow_html=True)

# --- LISTA COMPLETA DE PREGUNTAS ---
PREGUNTAS_CUIDADO = [
    "Hablaba conmigo con voz cálida y amistosa.", "No me ayudaba tanto como necesitaba.",
    "Parecía entender mis problemas.", "Era afectuoso/a conmigo.",
    "Disfrutaba charlando conmigo.", "Me sonreía frecuentemente.",
    "Me hacía sentir mejor cuando estaba triste.", "No hablaba mucho conmigo.",
    "Parecía frío/a emocionalmente.", "No entendía lo que yo quería.",
    "Me hacía sentir que no era querido/a.", "No me daba elogios."
]

PREGUNTAS_SOBREP = [
    "Me dejaba hacer cosas que me gustaban.", "Me dejaba tomar mis propias decisiones.",
    "Me dejaba decidir por mí mismo/a.", "Me daba más libertad de la que quería.",
    "Me dejaba salir seguido.", "Me dejaba vestirme como quería.",
    "No quería que creciera.", "Intentaba controlar todo lo que hacía.",
    "Invadía mi privacidad.", "Me trataba como a un bebé.",
    "Intentaba hacerme dependiente.", "Sentía que no podía cuidarme solo/a.", "Era sobreprotector/a."
]

def obtener_resultado(c, s):
    # Lógica de interpretación
    if c >= 24 and s < 12.5:
        return "Óptimo", "Vínculo Seguro", "Alta calidez y autonomía. Personalidad resiliente.", "Óptimo"
    elif c >= 24 and s >= 12.5:
        return "Cariñoso", "Control Cariñoso", "Afecto intrusivo. Riesgo de dependencia emocional.", "Óptimo"
    elif c < 24 and s < 12.5:
        return "Débil", "Vínculo Débil", "Frialdad afectiva y desapego.", "Crítico"
    else:
        return "Crítico", "Control Sin Afecto", "Alto riesgo: Rechazo y rigidez. Posible ansiedad/depresión.", "Crítico"

# --- INTERFAZ ---
nombre = st.text_input("Nombre del Evaluado:")
opcion = st.radio("Crianza:", ["Ambos Padres", "Solo Madre", "Solo Padre"], horizontal=True)

opciones_pbi = [0, 1, 2, 3]
formato = lambda x: ["Muy de acuerdo", "De acuerdo", "En desacuerdo", "Muy en desacuerdo"][x]

res_m_c, res_m_s = [], []
res_p_c, res_p_s = [], []

# Columnas para organizar
if "Madre" in opcion or "Ambos" in opcion:
    st.header("👩 Evaluación de la Madre")
    col1, col2 = st.columns(2)
    with col1:
        for p in PREGUNTAS_CUIDADO: res_m_c.append(st.radio(f"M-Cuidado: {p}", opciones_pbi, format_func=formato, key=f"mc_{p}"))
    with col2:
        for p in PREGUNTAS_SOBREP: res_m_s.append(st.radio(f"M-Sobreprotección: {p}", opciones_pbi, format_func=formato, key=f"ms_{p}"))

if "Padre" in opcion or "Ambos" in opcion:
    st.header("👨 Evaluación del Padre")
    col3, col4 = st.columns(2)
    with col3:
        for p in PREGUNTAS_CUIDADO: res_p_c.append(st.radio(f"P-Cuidado: {p}", opciones_pbi, format_func=formato, key=f"pc_{p}"))
    with col4:
        for p in PREGUNTAS_SOBREP: res_p_s.append(st.radio(f"P-Sobreprotección: {p}", opciones_pbi, format_func=formato, key=f"ps_{p}"))

# --- RESULTADOS ---
if st.button("📊 GENERAR DIAGNÓSTICO Y ANIMACIONES"):
    st.balloons()
    
    def mostrar_info(figura, c_list, s_list):
        pc, ps = sum(c_list), sum(s_list)
        tipo, titulo, desc, anim_key = obtener_resultado(pc, ps)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            anim = load_lottieurl(ANIMACIONES.get(anim_key, "https://lottie.host"))
            st_lottie(anim, height=250, key=f"lottie_{figura}")
        with c2:
            st.markdown(f"""
                <div class="resultado-card">
                    <h2>Resultado {figura}: {titulo}</h2>
                    <p><b>Puntajes:</b> Cuidado: {pc} | Sobreprotección: {ps}</p>
                    <p><b>Interpretación:</b> {desc}</p>
                </div>
                """, unsafe_allow_html=True)

    if res_m_c: mostrar_info("Madre", res_m_c, res_m_s)
    if res_p_c: mostrar_info("Padre", res_p_c, res_p_s)
