import streamlit as st
from fpdf import FPDF
import base64

# --- CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="PBI - Honduras", page_icon="🧠", layout="wide")

def add_bg_and_logos():
    # Fondo con temática de psicología (suave) y logos
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), 
                        url("https://transparenttextures.com");
            background-color: #f0f4f7;
        }}
        [data-testid="stSidebar"] {{
            background-color: #003366;
        }}
        .header-box {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_and_logos()

# --- ENCABEZADO INSTITUCIONAL ---
st.markdown("""
    <div class="header-box">
        <img src="https://wikimedia.org" width="80">
        <div style="text-align: center;">
            <h2 style="margin:0; color:#003366;">POLICÍA NACIONAL DE HONDURAS</h2>
            <p style="margin:0; color:#555;">Unidad de Psicología - Parental Bonding Instrument (PBI)</p>
        </div>
        <img src="https://wikimedia.org" width="60">
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
BLOQUES = {
    "Sobreprotección (Baja/Fomento Independencia)": [
        "Me dejaba hacer las cosas que me gustaban.", "Le gustaba que yo tomara mis propias decisiones.",
        "Me dejaba decidir las cosas por mí mismo.", "Me daba más libertad de la que yo quería.",
        "Me dejaba salir tan a menudo como yo deseaba.", "Dejaba que me vistiera como a mí me gustaba."
    ],
    "Sobreprotección (Alta/Control-Intrusión)": [
        "No quería que yo creciera.", "Intentaba controlar todo lo que yo hacía.",
        "Invadía mi vida privada.", "Tendía a tratarme como a un/a niño/a.",
        "Intentaba hacerme dependiente de él/ella.", 
        "Sentía que yo no podía cuidar de mí mismo/a a no ser que él/ella estuviera cerca.",
        "Era sobre-protector/a conmigo."
    ],
    "Cuidado (Calidez/Afecto)": [
        "Hablaba conmigo en un tono de voz cálido y amistoso.", "No me ayudaba tanto como yo necesitaba.",
        "Parecía entender mis problemas y preocupaciones.", "Era afectuoso/a conmigo.",
        "Disfrutaba charlando conmigo.", "Me sonreía frecuentemente.",
        "Podía hacer que me sintiera mejor cuando me encontraba contrariado.", "No hablaba mucho conmigo."
    ],
    "Cuidado (Frialdad/Rechazo)": [
        "Conmigo parecía emocionalmente frío/a.", "No parecía entender lo que yo quería o necesitaba.",
        "Me hacía sentir que no era querido.", "No me decía palabras de elogio"
    ]
}

def calcular_puntos(respuestas, bloque_tipo):
    total = 0
    # Leyendas del PDF: (0-3) o (3-0)
    for r in respuestas:
        if bloque_tipo in ["Sobreprotección (Baja/Fomento Independencia)", "Cuidado (Frialdad/Rechazo)"]:
            total += r # 0=Acuerdo, 3=Desacuerdo
        else:
            total += (3 - r) # 3=Acuerdo, 0=Desacuerdo
    return total

def interpretar_resultado(c, s):
    # Puntos de corte según Parker (Cuidado: 27 Madre / 24 Padre | Sobre: 13.5 Madre / 12.5 Padre)
    if c >= 24 and s <= 13:
        return "Óptimo", "Alta calidez y autonomía.", "Fomenta seguridad, alta autoestima y resiliencia."
    elif c < 24 and s <= 13:
        return "Ausente o Débil", "Baja calidez y baja sobreprotección.", "Riesgo de sentimientos de soledad, desapego emocional e inseguridad."
    elif c >= 24 and s > 13:
        return "Constreñido (Control Cariñoso)", "Alta calidez pero intrusivo.", "Dificulta la toma de decisiones independiente y genera dependencia emocional."
    else:
        return "Control Sin Afecto (ALTO RIESGO)", "Bajo cuidado y alto control.", "Asociado a ansiedad, depresión, rechazo y falta de habilidades de afrontamiento."

# --- FORMULARIO ---
st.write("---")
nombre = st.text_input("Nombre del evaluado/a:")
opcion_crianza = st.radio("Crianza:", ["Ambos Padres", "Solo Madre", "Solo Padre"], horizontal=True)

evaluar_madre = opcion_crianza in ["Ambos Padres", "Solo Madre"]
evaluar_padre = opcion_crianza in ["Ambos Padres", "Solo Padre"]

res_m, res_p = {}, {}

tabs = []
if evaluar_madre: tabs.append("Madre")
if evaluar_padre: tabs.append("Padre")

tab_objs = st.tabs(tabs)

for i, tab_label in enumerate(tabs):
    with tab_objs[i]:
        for bloque, preguntas in BLOQUES.items():
            st.subheader(bloque)
            for p in preguntas:
                res = st.select_slider(p, options=[0, 1, 2, 3], 
                    value=1, format_func=lambda x: ["Muy de acuerdo", "De acuerdo", "En desacuerdo", "Muy en desacuerdo"][x],
                    key=f"{tab_label}_{p}")
                if tab_label == "Madre": res_m[p] = res
                else: res_p[p] = res

if st.button("Generar Informe Psicológico"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "INFORME DE VÍNCULO PARENTAL (PBI)", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Nombre: {nombre}", ln=True)
    pdf.cell(0, 10, f"Modalidad: {opcion_crianza}", ln=True)
    pdf.ln(5)

    def agregar_resultado_pdf(figura, res_dict):
        c = calcular_puntos([res_dict[p] for p in BLOQUES["Cuidado (Calidez/Afecto)"]], "Cuidado (Calidez/Afecto)") + \
            calcular_puntos([res_dict[p] for p in BLOQUES["Cuidado (Frialdad/Rechazo)"]], "Cuidado (Frialdad/Rechazo)")
        s = calcular_puntos([res_dict[p] for p in BLOQUES["Sobreprotección (Baja/Fomento Independencia)"]], "Sobreprotección (Baja/Fomento Independencia)") + \
            calcular_puntos([res_dict[p] for p in BLOQUES["Sobreprotección (Alta/Control-Intrusión)"]], "Sobreprotección (Alta/Control-Intrusión)")
        
        tipo, desc, cons = interpretar_resultado(c, s)
        pdf.set_font("Arial", 'B', 14)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, f"RESULTADOS: {figura.upper()}", ln=True, fill=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"Puntaje Cuidado: {c} | Sobreprotección: {s}", ln=True)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, f"Tipo de Vínculo: {tipo}", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 8, f"Descripción: {desc}")
        pdf.multi_cell(0, 8, f"Consecuencias: {cons}")
        pdf.ln(5)

    if evaluar_madre: agregar_resultado_pdf("Madre", res_m)
    if evaluar_padre: agregar_resultado_pdf("Padre", res_p)

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button("📥 Descargar Reporte Final", data=pdf_bytes, file_name=f"PBI_Honduras_{nombre}.pdf")
