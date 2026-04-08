import streamlit as st
from fpdf import FPDF

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PBI - Policía Nacional de Honduras", page_icon="👮", layout="wide")

# CSS para corregir visibilidad y forzar colores legibles
st.markdown("""
    <style>
    /* Forzar fondo claro y texto oscuro en toda la app */
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    /* Estilo del encabezado institucional */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #002244; /* Azul oscuro policial */
        padding: 20px;
        border-radius: 15px;
        color: white !important;
        margin-bottom: 30px;
        border: 2px solid #001122;
    }
    .header-container h1, .header-container h3 {
        color: white !important;
        margin: 0;
    }
    /* Forzar que las etiquetas de las preguntas sean negras y visibles */
    label, p, span, .stMarkdown {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    /* Estilo para los sliders y radios */
    .stSelectSlider div {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO CON LOGOS ---
st.markdown("""
    <div class="header-container">
        <img src="https://wikimedia.org" width="90">
        <div style="text-align: center;">
            <h1>POLICÍA NACIONAL DE HONDURAS</h1>
            <h3>Unidad de Psicología - Evaluación PBI</h3>
        </div>
        <img src="https://wikimedia.org" width="70">
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE PREGUNTAS (Basada en el modelo oficial) ---
PREGUNTAS_CUIDADO = [
    "Hablaba conmigo con voz cálida y amistosa.", "No me ayudaba tanto como necesitaba.",
    "Parecía entender mis problemas y preocupaciones.", "Era afectuoso/a conmigo.",
    "Disfrutaba charlando conmigo.", "Me sonreía frecuentemente.",
    "Podía hacer que me sintiera mejor cuando estaba triste.", "No hablaba mucho conmigo.",
    "Parecía frío/a emocionalmente.", "No parecía entender lo que quería o necesitaba.",
    "Me hacía sentir que no era querido/a.", "No me daba elogios."
]

PREGUNTAS_SOBREP = [
    "Me dejaba hacer cosas que me gustaban.", "Le gustaba que tomara mis propias decisiones.",
    "Me dejaba decidir por mí mismo/a.", "Me daba más libertad de la que quería.",
    "Me dejaba salir tan seguido como quería.", "Me dejaba vestirme como quería.",
    "No quería que creciera.", "Intentaba controlar todo lo que hacía.",
    "Invadía mi privacidad.", "Me trataba como a un bebé.",
    "Intentaba hacerme dependiente.", "Sentía que no podía cuidarme solo/a.", "Era sobreprotector/a."
]

def interpretar_pbi(c, s):
    if c >= 24 and s < 12.5:
        return "Vínculo Óptimo", "Alta calidez y autonomía.", "Consecuencias: Personalidad segura, buena autoestima y relaciones sanas."
    elif c >= 24 and s >= 12.5:
        return "Control Cariñoso", "Afecto presente pero con sobreprotección.", "Consecuencias: Dependencia emocional y dificultad para decidir solo."
    elif c < 24 and s < 12.5:
        return "Vínculo Débil", "Bajo afecto y poca supervisión.", "Consecuencias: Sentimientos de soledad y frialdad afectiva."
    else:
        return "Control Sin Afecto (Riesgo)", "Bajo afecto y alto control.", "Consecuencias: Riesgo de ansiedad, depresión y sentimientos de rechazo."

# --- INTERFAZ DE USUARIO ---
st.write("### 📋 Datos Generales")
nombre = st.text_input("Nombre completo del evaluado:")
opcion = st.radio("Configuración familiar:", ["Ambos Padres", "Solo Madre", "Solo Padre"], horizontal=True)

res_m_c, res_m_s = [], []
res_p_c, res_p_s = [], []

# Formulario Madre
if "Madre" in opcion or "Ambos" in opcion:
    st.markdown("---")
    st.header("👩 Evaluación de la Madre")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Escala de Cuidado")
        for p in PREGUNTAS_CUIDADO:
            res_m_c.append(st.radio(f"M-C: {p}", [0,1,2,3], format_func=lambda x: ["Muy de acuerdo", "De acuerdo", "En desacuerdo", "Muy en desacuerdo"][x], key=f"mc_{p}"))
    with col2:
        st.subheader("Sobreprotección")
        for p in PREGUNTAS_SOBREP:
            res_m_s.append(st.radio(f"M-S: {p}", [0,1,2,3], format_func=lambda x: ["Muy de acuerdo", "De acuerdo", "En desacuerdo", "Muy en desacuerdo"][x], key=f"ms_{p}"))

# Formulario Padre
if "Padre" in opcion or "Ambos" in opcion:
    st.markdown("---")
    st.header("👨 Evaluación del Padre")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Escala de Cuidado")
        for p in PREGUNTAS_CUIDADO:
            res_p_c.append(st.radio(f"P-C: {p}", [0,1,2,3], format_func=lambda x: ["Muy de acuerdo", "De acuerdo", "En desacuerdo", "Muy en desacuerdo"][x], key=f"pc_{p}"))
    with col4:
        st.subheader("Sobreprotección")
        for p in PREGUNTAS_SOBREP:
            res_p_s.append(st.radio(f"P-S: {p}", [0,1,2,3], format_func=lambda x: ["Muy de acuerdo", "De acuerdo", "En desacuerdo", "Muy en desacuerdo"][x], key=f"ps_{p}"))

# --- BOTÓN DE RESULTADOS ---
if st.button("📊 Generar Reporte Final e Imprimir PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "REPORTE PSICOLÓGICO - PBI", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Paciente: {nombre}", ln=True)
    pdf.cell(0, 10, f"Crianza: {opcion}", ln=True)
    pdf.ln(10)

    def agregar_seccion(pdf, titulo, c_score, s_score):
        nivel, desc, cons = interpretar_pbi(sum(c_score), sum(s_score))
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"FIGURA: {titulo}", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"Cuidado: {sum(c_score)} | Sobreprotección: {sum(s_score)}", ln=True)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, f"Resultado: {nivel}", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 7, f"Interpretación: {desc}")
        pdf.multi_cell(0, 7, f"Consecuencias: {cons}")
        pdf.ln(5)

    if res_m_c: agregar_seccion(pdf, "MADRE", res_m_c, res_m_s)
    if res_p_c: agregar_seccion(pdf, "PADRE", res_p_c, res_p_s)

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button("📥 DESCARGAR PDF", data=pdf_bytes, file_name=f"PBI_{nombre}.pdf")
