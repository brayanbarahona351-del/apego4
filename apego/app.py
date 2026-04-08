import streamlit as st
from fpdf import FPDF
from streamlit_lottie import st_lottie
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="PBI Honduras - Psicología", page_icon="🧠", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# Animaciones según resultado
ANIMACIONES = {
    "Óptimo": "https://lottiefiles.com", # Corazón/Felicidad
    "Cariñoso": "https://lottiefiles.com", # Protección/Nudo
    "Débil": "https://lottiefiles.com", # Soledad/Viento
    "Crítico": "https://lottiefiles.com" # Alerta/Riesgo
}

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    .resultado-card {
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #003366;
        background-color: #f8f9fa;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .header-pnh {
        background-color: #002244;
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
    }
    label { color: black !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("""
    <div class="header-pnh">
        <h1>POLICÍA NACIONAL DE HONDURAS</h1>
        <p>Unidad de Psicología | Sistema de Evaluación PBI</p>
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA ---
PREGUNTAS_CUIDADO = ["Hablaba conmigo con voz cálida.", "Parecía entender mis problemas.", "Era afectuoso/a conmigo.", "Me sonreía frecuentemente."] # Resumido para el ejemplo
PREGUNTAS_SOBREP = ["No quería que creciera.", "Intentaba controlar todo.", "Invadía mi privacidad.", "Era sobreprotector/a."]

def obtener_resultado(c, s):
    if c >= 10: # Ajustado para menos preguntas en este ejemplo
        return ("Óptimo", "Vínculo Seguro", "Fomenta independencia.", "Óptimo") if s < 5 else ("Cariñoso", "Control Cariñoso", "Afecto intrusivo.", "Cariñoso")
    return ("Débil", "Vínculo Débil", "Frialdad afectiva.", "Débil") if s < 5 else ("Crítico", "Control Sin Afecto", "Alto riesgo psicológico.", "Crítico")

# --- INTERFAZ ---
nombre = st.text_input("Nombre del Evaluado:")
opcion = st.radio("Crianza:", ["Ambos Padres", "Solo Madre", "Solo Padre"], horizontal=True)

res_m_c, res_m_s = [], []
res_p_c, res_p_s = [], []

col_m, col_p = st.columns(2)

if "Madre" in opcion or "Ambos" in opcion:
    with col_m:
        st.header("👩 Madre")
        for p in PREGUNTAS_CUIDADO: res_m_c.append(st.radio(f"M: {p}", , key=f"mc_{p}"))
        for p in PREGUNTAS_SOBREP: res_m_s.append(st.radio(f"M: {p}", , key=f"ms_{p}"))

if "Padre" in opcion or "Ambos" in opcion:
    with col_p:
        st.header("👨 Padre")
        for p in PREGUNTAS_CUIDADO: res_p_c.append(st.radio(f"P: {p}", , key=f"pc_{p}"))
        for p in PREGUNTAS_SOBREP: res_p_s.append(st.radio(f"P: {p}", , key=f"ps_{p}"))

if st.button("📊 VER RESULTADOS Y ANIMACIONES"):
    st.divider()
    
    def mostrar_diagnostico(figura, c_list, s_list):
        p_c, p_s = sum(c_list), sum(s_list)
        tipo, titulo, desc, anim_key = obtener_resultado(p_c, p_s)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            lottie_anim = load_lottieurl(ANIMACIONES[anim_key])
            st_lottie(lottie_anim, height=200, key=f"anim_{figura}")
        with c2:
            st.markdown(f"""
                <div class="resultado-card">
                    <h3>Resultado {figura}: {titulo}</h3>
                    <p><b>Puntajes:</b> Cuidado: {p_c} | Sobreprotección: {p_s}</p>
                    <p><b>Interpretación:</b> {desc}</p>
                    <p><i>Análisis: Este nivel sugiere intervenciones enfocadas en fortalecer la autonomía del paciente.</i></p>
                </div>
                """, unsafe_allow_html=True)

    if res_m_c: mostrar_diagnostico("Madre", res_m_c, res_m_s)
    if res_p_c: mostrar_diagnostico("Padre", res_p_c, res_p_s)

    st.balloons() # Animación final de celebración
