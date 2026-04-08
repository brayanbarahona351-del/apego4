import streamlit as st
from fpdf import FPDF
from streamlit_lottie import st_lottie
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PBI Honduras - Psicología", page_icon="👮", layout="wide")

# Forzar visibilidad (Fondo blanco, texto negro) para evitar distorsiones de tema
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

# Función para cargar animaciones con validación (Evita el error de la imagen)
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

ANIMACIONES = {
    "Óptimo": "https://lottie.host",
    "Crítico": "https://lottie.host"
}

# --- ENCABEZADO INSTITUCIONAL ---
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
    "Podía hacerme sentir mejor cuando estaba triste.", "No hablaba mucho conmigo.",
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
    # Puntos de corte oficiales (Parker): Madre 27/13.5 | Padre 24/12.5
    cut_c = 27 if figura == "Madre" else 24
    cut_s = 13.5 if figura == "Madre" else 12.5
    
    if c >= cut_c and s < cut_s:
        return "Vínculo Óptimo", "Alta calidez y autonomía.", "Consecuencias: Alta autoestima, resiliencia y relaciones saludables.", "Óptimo"
    elif c >= cut_c and s >= cut_s:
        return "Control Cariñoso", "Afecto con sobreprotección.", "Consecuencias: Dependencia emocional y dificultad en toma de decisiones.", "Óptimo"
    elif c < cut_c and s < cut_s:
        return "Vínculo Débil", "Frialdad afectiva y desapego.", "Consecuencias: Sentimientos de soledad e inseguridad afectiva.", "Crítico"
    else:
        return "Control Sin Afecto", "Alto riesgo: Rechazo y control rígido.", "Consecuencias: Alto riesgo de ansiedad, depresión y baja autoestima crónica.", "Crítico"

# --- FORMULARIO ---
nombre = st.text_input("Nombre del Evaluado:")
opcion = st.radio("Configuración de crianza:", ["Ambos Padres", "Solo Madre", "Solo Padre"], horizontal=True)

opciones_radio = 
formato_pbi = lambda x: ["Muy de acuerdo", "De acuerdo", "En desacuerdo", "Muy en desacuerdo"][x]

res_m_c, res_m_s = [], []
res_p_c, res_p_s = [], []

if "Madre" in opcion or "Ambos" in opcion:
    with st.expander("📝 EVALUACIÓN DE LA MADRE", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            for p in PREGUNTAS_CUIDADO: res_m_c.append(st.radio(f"M-C: {p}", opciones_radio, format_func=formato_pbi, key=f"mc_{p}"))
        with col2:
            for p in PREGUNTAS_SOBREP: res_m_s.append(st.radio(f"M-S: {p}", opciones_radio, format_func=formato_pbi, key=f"ms_{p}"))

if "Padre" in opcion or "Ambos" in opcion:
    with st.expander("📝 EVALUACIÓN DEL PADRE", expanded=True):
        col3, col4 = st.columns(2)
        with col3:
            for p in PREGUNTAS_CUIDADO: res_p_c.append(st.radio(f"P-C: {p}", opciones_radio, format_func=formato_pbi, key=f"pc_{p}"))
        with col4:
            for p in PREGUNTAS_SOBREP: res_p_s.append(st.radio(f"P-S: {p}", opciones_radio, format_func=formato_pbi, key=f"ps_{p}"))

# --- PROCESAMIENTO ---
if st.button("📊 GENERAR DIAGNÓSTICO FINAL"):
    st.balloons()
    
    def mostrar_diagnostico(figura, c_list, s_list):
        pc, ps = sum(c_list), sum(s_list)
        tipo, titulo, cons, anim_key = obtener_resultado(pc, ps, figura)
        
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
                    <p><b>Descripción:</b> {titulo}</p>
                    <p><b>Análisis Clínico:</b> {cons}</p>
                </div>
                """, unsafe_allow_html=True)

    if res_m_c: mostrar_diagnostico("Madre", res_m_c, res_m_s)
    if res_p_c: mostrar_diagnostico("Padre", res_p_c, res_p_s)

    # Generar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "POLICÍA NACIONAL DE HONDURAS - REPORTE PBI", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Nombre: {nombre}", ln=True)
    pdf.ln(10)
    
    def add_pdf_sec(fig, c_l, s_l):
        pc, ps = sum(c_l), sum(s_l)
        tipo, tit, cons, _ = obtener_resultado(pc, ps, fig)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"FIGURA: {fig}", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"Cuidado: {pc} | Sobreprotección: {ps}", ln=True)
        pdf.cell(0, 8, f"Nivel: {tipo}", ln=True)
        pdf.multi_cell(0, 7, f"Análisis: {cons}")
        pdf.ln(5)

    if res_m_c: add_pdf_sec("Madre", res_m_c, res_m_s)
    if res_p_c: add_pdf_sec("Padre", res_p_c, res_p_s)
    
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button("📥 DESCARGAR INFORME PDF", data=pdf_bytes, file_name=f"PBI_{nombre}.pdf")
