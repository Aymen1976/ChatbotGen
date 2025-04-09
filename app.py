 import streamlit as st
from reportlab.pdfgen import canvas
import io

def generate_pdf(titre, date, contenu):
    if not titre or not date or not contenu:
        return None
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    textobject = c.beginText(100, 750)
    textobject.setFont("Helvetica", 12)
    textobject.textLine(f"Titre: {titre}")
    textobject.textLine(f"Date: {date}")
    textobject.textLine("")
    for line in contenu.split("\n"):
        textobject.textLine(line)
    c.drawText(textobject)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

st.title("Générateur de PDF")

titre = st.text_input("Titre du document", "Document généré par Chatbot")
date = st.text_input("Date", "08/03/2025")
contenu = st.text_area("Contenu", "Ceci est un test")

if st.button("Générer PDF"):
    pdf_file = generate_pdf(titre, date, contenu)
    if pdf_file:
        st.download_button("Télécharger le PDF", data=pdf_file, file_name="document_chatbot.pdf", mime="application/pdf")
    else:
        st.error("Veuillez remplir tous les champs avant de générer le PDF.")

