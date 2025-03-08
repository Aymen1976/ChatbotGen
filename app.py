import streamlit as st
from reportlab.pdfgen import canvas
import io

# Fonction pour générer le PDF
def generate_pdf(titre, date, contenu):
    buffer = io.BytesIO()  # Crée un buffer mémoire pour le PDF
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, f"Titre: {titre}")
    c.drawString(100, 730, f"Date: {date}")
    c.drawString(100, 710, "Contenu:")
    
    y_position = 690
    for line in contenu.split("\n"):
        c.drawString(100, y_position, line)
        y_position -= 20
    
    c.save()
    buffer.seek(0)  # Revenir au début du fichier
    return buffer

# Interface Streamlit
st.title("Générateur de PDF")

titre = st.text_input("Titre du document", "Document généré par Chatbot")
date = st.text_input("Date", "08/03/2025")
contenu = st.text_area("Contenu", "Ceci est un test")

if st.button("Générer PDF"):
    pdf_file = generate_pdf(titre, date, contenu)
    st.download_button(label="Télécharger le PDF", data=pdf_file, file_name="document_chatbot.pdf", mime="application/pdf")
