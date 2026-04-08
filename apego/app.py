import streamlit as st
from fpdf import FPDF

# --- DATOS DEL MODELO PDF ---
BLOQUES = {
    "Sobreprotección - Baja": [
        "Me dejaba hacer las cosas que me gustaban.",
        "Le gustaba que yo tomara mis propias decisiones.",
        "Me dejaba decidir las cosas por mí mismo.",
        "Me daba más libertad de la que yo quería.",
        "Me dejaba salir tan a menudo como yo deseaba.",
        "Dejaba que me vistiera como a mí me gustaba."
    ],
    "Sobreprotección - Alta": [
        "No quería que yo creciera.",
        "Intentaba controlar todo lo que yo hacía.",
        "Invadía mi vida privada.",
        "Tendía a tratarme como a un/a niño/a.",
        "Intentaba hacerme dependiente de él/ella.",
        "Sentía que yo no podía cuidar de mí mismo/a a no ser que él/ella estuviera cerca.",
        "Era sobre-protector/a conmigo."
    ],
    "Cuidado - Positivo": [
        "Hablaba conmigo en un tono de voz cálido y amistoso.",
        "No me ayudaba tanto como yo necesitaba.",
        "Parecía entender mis problemas y preocupaciones.",
        "Era afectuoso/a conmigo.",
        "Disfrutaba charlando conmigo.",
        "Me sonreía frecuentemente.",
        "Podía hacer que me sintiera mejor cuando me encontraba contrariado.",
        "No hablaba mucho conmigo."
    ],
    "Cuidado - Negativo": [
        "Conmigo parecía emocionalmente frío/a.",
        "No parecía entender lo que yo quería o necesitaba.",
        "Me hacía sentir que no era querido.",
        "No me decía palabras de elogio"
    ]
}

# --- FUNCIONES DE CÁLCULO ---
def calcular_puntos(respuestas, bloque_tipo):
    total = 0
    # Modelo 0-3 o 3-0 según el PDF
    mapping_03 = {0: 0, 1: 1, 2: 2, 3: 3}
    mapping_30 = {0: 3, 1: 2, 2: 1, 3: 0}
    
    for r in respuestas:
        if bloque_tipo in ["Sobreprotección - Baja", "Cuidado - Negativo"]:
            total += mapping_03[r]
        else:
            total += mapping_30[r]
    return total

def obtener_vinculo(cuidado, sobrep):
    # Umbrales basados en puntuaciones medias (ajustables según baremos locales)
    if cuidado >= 24 and sobrep < 12:
        return "Óptimo", "Alta calidez y fomento de la autonomía.", "Desarrollo de una autoestima sana y seguridad personal."
    elif cuidado < 24 and sobrep < 12:
        return "Ausente o débil", "Bajo cuidado y baja sobreprotección.", "Posible sentimiento de desapego o indiferencia afectiva."
    elif cuidado >= 24 and sobrep >= 12:
        return "Constreñido", "Alto cuidado y alta sobreprotección.", "Dificultad para desarrollar independencia a pesar del afecto."
    else:
        return "Control sin afecto", "Bajo cuidado y alta sobreprotección (Alto Riesgo).", "Relacionado con rechazo, frialdad e intrusión; riesgo de ansiedad y baja autonomía."

# --- INTERFAZ ---
st.title("PBI: Parental Bonding Instrument")
nombre_paciente = st.text_input("Nombre del evaluado/a:")

col1, col2 = st.columns(2)
with col1:
    st.header("Evaluación: PADRE")
    res_p = {}
    for bloque, preguntas in BLOQUES.items():
        st.subheader(bloque)
        for p in preguntas:
            res_p[p] = st.radio(p, [0, 1, 2, 3], format_func=lambda x: ["Muy de acuerdo", "De acuerdo", "En desacuerdo", "Muy en desacuerdo"][x], key=f"p_{p}")

with col2:
    st.header("Evaluación: MADRE")
    res_m = {}
    for bloque, preguntas in BLOQUES.items():
        st.subheader(bloque)
        for p in preguntas:
            res_m[p] = st.radio(p, [0, 1, 2, 3], format_func=lambda x: ["Muy de acuerdo", "De acuerdo", "En desacuerdo", "Muy en desacuerdo"][x], key=f"m_{p}")

if st.button("Calcular y Generar Reporte"):
    # Cálculos Padre
    s_p = calcular_puntos([res_p[p] for p in BLOQUES["Sobreprotección - Baja"]], "Sobreprotección - Baja") + \
          calcular_puntos([res_p[p] for p in BLOQUES["Sobreprotección - Alta"]], "Sobreprotección - Alta")
    c_p = calcular_puntos([res_p[p] for p in BLOQUES["Cuidado - Positivo"]], "Cuidado - Positivo") + \
          calcular_puntos([res_p[p] for p in BLOQUES["Cuidado - Negativo"]], "Cuidado - Negativo")
    
    # Cálculos Madre
    s_m = calcular_puntos([res_m[p] for p in BLOQUES["Sobreprotección - Baja"]], "Sobreprotección - Baja") + \
          calcular_puntos([res_m[p] for p in BLOQUES["Sobreprotección - Alta"]], "Sobreprotección - Alta")
    c_m = calcular_puntos([res_m[p] for p in BLOQUES["Cuidado - Positivo"]], "Cuidado - Positivo") + \
          calcular_puntos([res_m[p] for p in BLOQUES["Cuidado - Negativo"]], "Cuidado - Negativo")

    # PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Reporte PBI - {nombre_paciente}", ln=True, align='C')
    
    for figura, c, s in [("PADRE", c_p, s_p), ("MADRE", c_m, s_m)]:
        tipo, desc, cons = obtener_vinculo(c, s)
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"FIGURA: {figura}", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"Puntaje Cuidado: {c} | Sobreprotección: {s}", ln=True)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, f"Tipo de Vínculo: {tipo}", ln=True)
        pdf.set_font("Arial", 'I', 11)
        pdf.multi_cell(0, 8, f"Características: {desc}")
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 8, f"Consecuencias/Riesgos: {cons}")
        pdf.ln(2)

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.download_button("📥 Descargar Reporte PDF", data=pdf_output, file_name=f"PBI_{nombre_paciente}.pdf")
