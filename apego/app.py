import streamlit as st
from fpdf import FPDF
from streamlit_lottie import st_lottie
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PBI Honduras - Psicología", page_icon="👮", layout="wide")

# CSS para forzar legibilidad y diseño institucional
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
                <h3>Unidad de Psicología | Evaluación PBI Completa</h3>
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

OPCIONES_TEXTO = {0: "Muy de acuerdo", 1: "De acuerdo", 2: "En desacuerdo", 3: "Muy en desacuerdo"}

def obtener_resultado(c, s, figura):
    cut_c = 27 if figura == "Madre" else 24
    cut_s = 13.5 if figura == "Madre" else 12.5
    if c >= cut_c and s < cut_s:
        return "Vínculo Óptimo", "Alta calidez y fomento de autonomía.", "Alta autoestima y resiliencia.", "Óptimo"
    elif c >= cut_c and s >= cut_s:
        return "Control Cariñoso", "Afecto con sobreprotección excesiva.", "Riesgo de dependencia emocional y timidez.", "Óptimo"
    elif c < cut_c and s < cut_s:
        return "Vínculo Débil / Ausente", "Baja calidez y bajo control (desapego).", "Sentimientos de soledad y dificultad de conexión.", "Crítico"
    else:
        return "Control Sin Afecto", "Baja calidez y alta sobreprotección.", "Alto riesgo de ansiedad, depresión y rechazo.", "Crítico"

# --- INTERFAZ ---
nombre = st.text_input("Nombre completo del evaluado/a:")
opcion = st.radio("Configuración de crianza:", ["Ambos Padres", "Solo Madre", "Solo Padre"], horizontal=True)

res_m_c, res_m_s = [], []
res_p_c, res_p_s = [], []

if "Madre" in opcion or "Ambos" in opcion:
    with st.expander("📝 EVALUACIÓN DE LA MADRE", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            for p in PREGUNTAS_CUIDADO: res_m_c.append(st.radio(f"M: {p}", [0,1,2,3], format_func=lambda x: OPCIONES_TEXTO[x], key=f"mc_{p}"))
        with c2:
            for p in PREGUNTAS_SOBREP: res_m_s.append(st.radio(f"M: {p}", [0,1,2,3], format_func=lambda x: OPCIONES_TEXTO[x], key=f"ms_{p}"))

if "Padre" in opcion or "Ambos" in opcion:
    with st.expander("📝 EVALUACIÓN DEL PADRE", expanded=True):
        c3, c4 = st.columns(2)
        with c3:
            for p in PREGUNTAS_CUIDADO: res_p_c.append(st.radio(f"P: {p}", [0,1,2,3], format_func=lambda x: OPCIONES_TEXTO[x], key=f"pc_{p}"))
        with c4:
            for p in PREGUNTAS_SOBREP: res_p_s.append(st.radio(f"P: {p}", [0,1,2,3], format_func=lambda x: OPCIONES_TEXTO[x], key=f"ps_{p}"))

# --- RESULTADOS Y PDF ---
if st.button("📊 GENERAR DIAGNÓSTICO E INFORME COMPLETO"):
    st.balloons()
    
    # Mostrar resultados en pantalla con animaciones
    def mostrar_info(fig, c_l, s_l):
        pc, ps = sum(c_l), sum(s_l)
        tipo, tit, cons, anim_k = obtener_resultado(pc, ps, fig)
        col_a, col_t = st.columns(2)
        with col_a:
            data = load_lottieurl(ANIMACIONES.get(anim_k))
            if data: st_lottie(data, height=250, key=f"a_{fig}")
            else: st.write("🧠")
        with col_t:
            st.markdown(f"""
                <div class="resultado-card">
                    <h2>Resultado {fig}: {tipo}</h2>
                    <p><b>Puntajes Brutos:</b> Cuidado: {pc} | Sobreprotección: {ps}</p>
                    <p><b>Diagnóstico:</b> {tit}</p>
                    <p><b>Consecuencias:</b> {cons}</p>
                </div>
            """, unsafe_allow_html=True)

    if res_m_c: mostrar_info("Madre", res_m_c, res_m_s)
    if res_p_c: mostrar_info("Padre", res_p_c, res_p_s)

    # Generación del PDF Detallado
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "POLICÍA NACIONAL DE HONDURAS - UNIDAD DE PSICOLOGÍA", ln=True, align='C')
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "INFORME DETALLADO DE VÍNCULO PARENTAL (PBI)", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Evaluado: {nombre}", ln=True)
    pdf.cell(0, 8, f"Crianza: {opcion}", ln=True)
    pdf.ln(5)

    def escribir_detalles(pdf, fig, c_l, s_l):
        pc, ps = sum(c_l), sum(s_l)
        tipo, tit, cons, _ = obtener_resultado(pc, ps, fig)
        
        pdf.set_fill_color(0, 34, 68)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f" RESULTADOS FIGURA: {fig.upper()}", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 8, f"DIAGNÓSTICO: {tipo}", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 8, f"Puntajes: Cuidado ({pc}) / Sobreprotección ({ps})", ln=True)
        pdf.multi_cell(0, 7, f"Análisis Clínico: {tit}")
        pdf.multi_cell(0, 7, f"Consecuencias en el desarrollo: {cons}")
        pdf.ln(5)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 8, "DETALLE DE RESPUESTAS:", ln=True)
        pdf.set_font("Arial", '', 9)
        # Unimos las listas de preguntas para el reporte
        todas_p = PREGUNTAS_CUIDADO + PREGUNTAS_SOBREP
        todas_r = c_l + s_l
        for i, p in enumerate(todas_p):
            pdf.multi_cell(0, 5, f"{i+1}. {p} -> Respuesta: {OPCIONES_TEXTO[todas_r[i]]}")
        pdf.ln(10)

    if res_m_c: escribir_detalles(pdf, "Madre", res_m_c, res_m_s)
    if res_p_c: escribir_detalles(pdf, "Padre", res_p_c, res_p_s)

    # Espacio para firma
    pdf.ln(10)
    pdf.cell(0, 10, "__________________________", ln=True, align='C')
    pdf.cell(0, 10, "Firma y Sello del Psicólogo/a", ln=True, align='C')

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button("📥 DESCARGAR INFORME COMPLETO (PDF)", data=pdf_bytes, file_name=f"Informe_PBI_{nombre}.pdf", mime="application/pdf")
