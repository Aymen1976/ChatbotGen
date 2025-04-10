from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit
from docx import Document

app = Flask(__name__)
OUTPUT_FOLDER = "output"
PDF_FOLDER = os.path.join(OUTPUT_FOLDER, "pdf")
DOCX_FOLDER = os.path.join(OUTPUT_FOLDER, "docx")

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(DOCX_FOLDER, exist_ok=True)

def generate_pdf(titre, date, contenu, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 2 * cm
    line_height = 14
    y = height - margin

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, titre)
    y -= 2 * line_height

    c.setFont("Helvetica", 12)
    c.drawString(margin, y, f"Date: {date}")
    y -= 2 * line_height

    lines = simpleSplit(contenu, "Helvetica", 12, width - 2 * margin)
    for line in lines:
        if y < margin + line_height:
            c.showPage()
            y = height - margin
            c.setFont("Helvetica", 12)
        c.drawString(margin, y, line)
        y -= line_height
    c.save()

def generate_docx(titre, date, contenu, output_path):
    doc = Document()
    doc.add_heading(titre, level=1)
    doc.add_paragraph(f"Date : {date}")
    doc.add_paragraph(contenu)
    doc.save(output_path)

@app.route("/")
def accueil():
    return "Bienvenue sur mon API ChatbotGen 🚀. Utilise /generer pour créer des documents."

@app.route("/generer", methods=["POST"])
def generer_documents():
    try:
        data = request.get_json()
        titre = data.get("titre", "Document sans titre")
        contenu = data.get("contenu", "")
        date = data.get("date", datetime.now().strftime("%Y-%m-%d"))

        if not contenu.strip():
            return jsonify({"error": "Le champ 'contenu' est requis"}), 400

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_pdf = f"{titre.replace(' ', '_')}_{timestamp}.pdf"
        nom_docx = f"{titre.replace(' ', '_')}_{timestamp}.docx"
        chemin_pdf = os.path.join(PDF_FOLDER, nom_pdf)
        chemin_docx = os.path.join(DOCX_FOLDER, nom_docx)

        generate_pdf(titre, date, contenu, chemin_pdf)
        generate_docx(titre, date, contenu, chemin_docx)

        return jsonify({
            "message": "✅ Fichiers générés avec succès",
            "pdf": f"/telecharger/pdf/{nom_pdf}",
            "docx": f"/telecharger/docx/{nom_docx}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/telecharger/pdf/<nom_fichier>")
def telecharger_pdf(nom_fichier):
    return send_from_directory(PDF_FOLDER, nom_fichier, as_attachment=True)

@app.route("/telecharger/docx/<nom_fichier>")
def telecharger_docx(nom_fichier):
    return send_from_directory(DOCX_FOLDER, nom_fichier, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
