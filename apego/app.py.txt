import streamlit as st
from fpdf import FPDF

# --- DATOS DE REFERENCIA ---
ITEMS_CUIDADO = [1, 2, 4, 5, 6, 11, 12, 13, 14, 16, 17, 18, 24]
ITEMS_SOBREP = [3, 7, 8, 9, 10, 15, 19, 20, 21, 22, 23, 25]
INVERSOS = [2, 4, 7, 14, 15, 16, 18, 21, 22, 24, 25]

PREGUNTAS = [
    "Me hablaba con voz amistosa y cálida.", "No me ayudaba tanto como yo lo necesitaba.",
    "Evitaba que yo saliera solo (a).", "Parecía emocionalmente fría hacia mí.",
    "Parecía entender mis problemas y preocupaciones.", "Era afectuosa conmigo.",
    "Le gustaba que tomara mis propias decisiones.", "No quería que creciera.",
    "Trataba de controlar todo lo que yo hacía.", "Invadía mi privacidad.",
    "Se entretenía conversando cosas conmigo.", "Me sonreía frecuentemente.",
    "Me regaloneaba.", "No parecía entender lo que yo quería o necesitaba.",
    "Me permitía decidir las cosas por mi mismo (a).", "Me hacía sentir que no era deseado.",
    "Tenía la capacidad de reconfortarme cuando me sentía molesto/a.", "No conversaba mucho conmigo.",
    "Trataba de hacerme dependiente de ella/él.", "Sentía que no podía cuidar de mi mismo (a), a menos que estuviera cerca.",
    "Me daba toda la libertad que yo quería.", "Me dejaba salir lo que yo quería.",
    "Era sobreprotectora conmigo.", "No me elogiaba.", "Me permitía vestirme como se me antojara."
]

OPCIONES_TEXTO = {1: "Muy en desacuerdo", 2: "Moderadamente en desacuerdo", 3: "Moderadamente de acuerdo", 4: "Muy de acuerdo"}

# --- LÓGICA ---
def calcular_puntuacion(respuestas):
    cuidado, sobrep = 0, 0
    for i, res in enumerate(respuestas):
        n_item = i + 1
        val = res - 1
        puntos = (3 - val) if n_item in INVERSOS else val
        if n_item in ITEMS_CUIDADO: cuidado += puntos
        elif n_item in ITEMS_SOBREP: sobrep += puntos
    return cuidado, sobrep

def obtener_interpretacion(c, s):
    if c >= 27.0:
        if s < 13.5: return "Vínculo Óptimo", "Alta calidez y autonomía.", "Fomentar la seguridad y el afecto."
        else: return "Control Cariñoso", "Alta calidez pero intrusivo.", "Trabajar en la independencia."
    else:
        if s < 13.5: return "Vínculo Débil / Desapego", "Baja calidez y baja protección.", "Mejorar la conexión emocional."
        else: return "Control Sin Afecto", "Baja calidez y alto control.", "Se sugiere apoyo profesional."

# --- GENERACIÓN DE PDF ---
def generar_pdf_completo(figura, respuestas, c, s, cat, desc, cons):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Reporte Detallado PBI - {figura}", ln=True, align='C')
    pdf.ln(5)

    # Resultados Resumidos
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, "RESUMEN DE RESULTADOS", ln=True, fill=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Puntaje Cuidado: {c} | Puntaje Sobreproteccion: {s}", ln=True)
    pdf.cell(0, 8, f"Categoria: {cat}", ln=True)
    pdf.multi_cell(0, 8, f"Consejo: {cons}")
    pdf.ln(5)

    # Detalle de Preguntas y Respuestas
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "DETALLE DE RESPUESTAS", ln=True, fill=True)
    pdf.set_font("Arial", size=9)
    
    for i, res in enumerate(respuestas):
        texto_pregunta = f"{i+1}. {PREGUNTAS[i]}"
        texto_respuesta = f"R: {OPCIONES_TEXTO[res]}"
        # Para evitar que el texto se corte
        pdf.multi_cell(0, 6, f"{texto_pregunta}")
        pdf.set_font("Arial", 'I', 9)
        pdf.cell(0, 5, f"   {texto_respuesta}", ln=True)
        pdf.set_font("Arial", size=9)
        pdf.ln(1)
        
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ STREAMLIT ---
st.title("📋 PBI: Cuestionario y Reporte")
figura = st.selectbox("Seleccione figura:", ["Madre", "Padre"])

respuestas_usuario = []
for idx, pregunta in enumerate(PREGUNTAS):
    res = st.radio(f"{idx+1}. {pregunta}", [1, 2, 3, 4], 
                   format_func=lambda x: OPCIONES_TEXTO[x], key=f"p{idx}")
    respuestas_usuario.append(res)

if st.button("Generar Reporte Completo"):
    pc, ps = calcular_puntuacion(respuestas_usuario)
    cat, desc, cons = obtener_interpretacion(pc, ps)
    
    st.divider()
    st.subheader("Vista Previa de Resultados")
    st.write(f"**Estilo:** {cat}")
    
    pdf_bytes = generar_pdf_completo(figura, respuestas_usuario, pc, ps, cat, desc, cons)
    
    st.download_button(
        label="📥 Descargar PDF con Preguntas y Respuestas",
        data=pdf_bytes,
        file_name=f"PBI_Detallado_{figura}.pdf",
        mime="application/pdf"
    )
