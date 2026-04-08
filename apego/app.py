import streamlit as st
from fpdf import FPDF
from streamlit_lottie import st_lottie
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PBI Honduras - Psicología", page_icon="👮", layout="wide")

# CSS para corregir visibilidad y diseño institucional
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; color: #000000 !important; }
    .header-pnh {
        background-color: #002244; color: white !important;
        padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 30px;
    }
    .resultado-card {
        padding: 20px; border-radius: 15px; border-left: 10px solid #003366;
        background-color: #f0f4f8; color: black; margin-bottom: 20px; box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }
    label, p, span, .stMarkdown { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

ANIMACIONES = {
    "Óptimo": "https://lottie.host",
    "Crítico": "https://lottie.host"
}

# --- ENCABEZADO ---
st.markdown("""
    <div class="header-pnh">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <img src="https://wikimedia.org" width="90">
            <div>
                <h1>POLICÍA NACIONAL DE HONDURAS</h1>
                <h3>Unidad de Psicología | Evaluación PBI</h3>
            </div>
            <img src="https://wikimedia.org" width="70">
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- PREGUNTAS ---
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

def obtener_resultado(c, s, figura):
    cut_c = 27 if figura == "Madre" else 24
    cut_s = 13.5 if figura == "Madre" else 12.5
    if c >= cut_c and s < cut_s:
        return "Vínculo Óptimo", "Alta calidez y autonomía.", "Seguridad y resiliencia.", "Óptimo"
    elif c >= cut_c and s >= cut_s:
        return "Control Cariñoso", "Afecto con sobreprotección.", "Dependencia emocional.", "Óptimo"
    elif c < cut_c and s < cut_s:
        return "Vínculo Débil", "Bajo afecto y bajo control.", "Desapego y soledad.", "Crítico"
    else:
        return "Control Sin Afecto", "Bajo afecto y alto control.", "Riesgo de ansiedad y depresión.", "Crítico"

# --- INTERFAZ ---
nombre = st.text_input("Nombre del evaluado:")
opcion = st.radio("Crianza:", ["Ambos Padres", "Solo Madre", "Solo Padre"], horizontal=True)

# CORRECCIÓN DE LA LÍNEA 86:
opciones_radio = [0, 1, 2, 3]
formato_pbi = lambda x: ["Muy de acuerdo", "De acuerdo", "En desacuerdo", "Muy en desacuerdo"][x]

res_m_c, res_m_s, res_p_c, res_p_s = [], [], [], []

if "Madre" in opcion or "Ambos" in opcion:
    with st.expander("EVALUACIÓN DE LA MADRE", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            for p in PREGUNTAS_CUIDADO: res_m_c.append(st.radio(f"M-C: {p}", opciones_radio, format_func=formato_pbi, key=f"mc_{p}"))
        with c2:
            for p in PREGUNTAS_SOBREP: res_m_s.append(st.radio(f"M-S: {p}", opciones_radio, format_func=formato_pbi, key=f"ms_{p}"))

if "Padre" in opcion or "Ambos" in opcion:
    with st.expander("EVALUACIÓN DEL PADRE", expanded=True):
        c3, c4 = st.columns(2)
        with c3:
            for p in PREGUNTAS_CUIDADO: res_p_c.append(st.radio(f"P-C: {p}", opciones_radio, format_func=formato_pbi, key=f"pc_{p}"))
        with c4:
            for p in PREGUNTAS_SOBREP: res_p_s.append(st.radio(f"P-S: {p}", opciones_radio, format_func=formato_pbi, key=f"ps_{p}"))

if st.button("📊 GENERAR DIAGNÓSTICO"):
    st.balloons()
    def mostrar_info(fig, c_l, s_l):
        pc, ps = sum(c_l), sum(s_l)
        tipo, tit, cons, anim_k = obtener_resultado(pc, ps, fig)
        col_a, col_t = st.columns(2)
        with col_a:
            data = load_lottieurl(ANIMACIONES.get(anim_k))
            if data: st_lottie(data, height=200, key=f"a_{fig}")
            else: st.write("🧠")
        with col_t:
            st.markdown(f'<div class="resultado-card"><h3>{fig}: {tipo}</h3><p>{tit}</p><p><i>{cons}</i></p></div>', unsafe_allow_html=True)

    if res_m_c: mostrar_info("Madre", res_m_c, res_m_s)
    if res_p_c: mostrar_info("Padre", res_p_c, res_p_s)
