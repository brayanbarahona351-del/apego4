import streamlit as st
from fpdf import FPDF
from streamlit_lottie import st_lottie
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PBI Honduras - Psicología", page_icon="👮", layout="wide")

# CSS para forzar fondo blanco, texto negro y diseño institucional
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; color: #000000 !important; }
    .header-pnh {
        background-color: #002244; color: white !important;
        padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 30px;
    }
    .header-pnh h1, .header-pnh h3 { color: white !important; margin: 0; }
    .resultado-card {
        padding: 20px; border-radius: 15px; border-left: 10px solid #003366;
        background-color: #f0f4f8; color: black; margin-bottom: 20px; box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }
    label, p, span, .stMarkdown { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# Función para cargar animaciones con seguridad
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

# Animaciones de Lottie
ANIMACIONES = {
    "Óptimo": "https://lottie.host",
    "Crítico": "https://lottie.host"
}

# --- ENCABEZADO CON LOGOS ---
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

# --- PREGUNTAS DEL MODELO ---
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
    # Puntos de corte: Madre 27/13.5 | Padre 24/12.5
    cut_c = 27 if figura == "Madre" else 24
    cut_s = 13.5 if figura == "Madre" else 12.5
    
    if c >= cut_c and s < cut_s:
        return "Vínculo Óptimo", "Alta calidez y autonomía.", "Desarrollo de una autoestima sana y seguridad personal.", "Óptimo"
    elif c >= cut_c and s >= cut_s:
        return "Control Cariñoso", "Afecto con sobreprotección.", "Dificultad para desarrollar independencia y seguridad propia.", "Óptimo"
    elif c < cut_c and s < cut_s:
        return "Vínculo Débil", "Frialdad afectiva y desapego.", "Riesgo de sentimientos de soledad y desapego emocional.", "Crítico"
    else:
        return "Control Sin Afecto", "Bajo afecto y alto control.", "Nivel crítico: Riesgo de ansiedad, depresión y sentimientos de rechazo.", "Crítico"

# --- INTERFAZ ---
nombre = st.text_input("Nombre completo del evaluado:")
opcion = st.radio("Seleccione la crianza:", ["Ambos Padres", "Solo Madre", "Solo Padre"], horizontal=True)

# AQUÍ SE CORRIGIÓ EL ERROR: Se agregaron los valores [0, 1, 2, 3]
opciones_radio = [0, 1, 2, 3]
formato_pbi = lambda x: ["Muy de acuerdo", "De acuerdo", "En desacuerdo", "Muy en desacuerdo"][x]

res_m_c, res_m_s = [], []
res_p_c, res_p_s = [], []

# Sección Madre
if "Madre" in opcion or "Ambos" in opcion:
    with st.expander("📝 EVALUACIÓN DE LA MADRE", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            for p in PREGUNTAS_CUIDADO: res_m_c.append(st.radio(f"M-Cuidado: {p}", opciones_radio, format_func=formato_pbi, key=f"mc_{p}"))
        with col2:
            for p in PREGUNTAS_SOBREP: res_m_s.append(st.radio(f"M-Sobrep.: {p}", opciones_radio, format_func=formato_pbi, key=f"ms_{p}"))

# Sección Padre
if "Padre" in opcion or "Ambos" in opcion:
    with st.expander("📝 EVALUACIÓN DEL PADRE", expanded=True):
        col3, col4 = st.columns(2)
        with col3:
            for p in PREGUNTAS_CUIDADO: res_p_c.append(st.radio(f"P-Cuidado: {p}", opciones_radio, format_func=formato_pbi, key=f"pc_{p}"))
        with col4:
            for p in PREGUNTAS_SOBREP: res_p_s.append(st.radio(f"P-Sobrep.: {p}", opciones_radio, format_func=formato_pbi, key=f"ps_{p}"))

# --- RESULTADOS ---
if st.button("📊 GENERAR RESULTADOS"):
    st.balloons()
    
    def mostrar_info(figura, c_list, s_list):
        pc, ps = sum(c_list), sum(s_list)
        tipo, tit, cons, anim_key = obtener_resultado(pc, ps, figura)
        
        c1, c2 = st.columns()
        with c1:
            anim_data = load_lottieurl(ANIMACIONES.get(anim_key))
            if anim_data: st_lottie(anim_data, height=250, key=f"anim_{figura}")
            else: st.write("🧠")
        with c2:
            st.markdown(f"""
                <div class="resultado-card">
                    <h2 style="color:#003366;">Resultado {figura}: {tipo}</h2>
                    <p><b>Puntajes:</b> Cuidado: {pc} | Sobreprotección: {ps}</p>
                    <p><b>Análisis:</b> {tit}</p>
                    <p><b>Consecuencias:</b> {cons}</p>
                </div>
                """, unsafe_allow_html=True)

    if res_m_c: mostrar_info("Madre", res_m_c, res_m_s)
    if res_p_c: mostrar_info("Padre", res_p_c, res_p_s)

    # Botón PDF simplificado
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "REPORTE PSICOLÓGICO PBI - POLICÍA NACIONAL", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Nombre: {nombre}", ln=True)
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button("📥 DESCARGAR PDF", data=pdf_bytes, file_name=f"PBI_{nombre}.pdf")
