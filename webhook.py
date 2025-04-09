import sys
sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, request, jsonify, send_file
import os
from datetime import datetime
from generate_document import generate_docx, generate_pdf  # Fonctions de génération

# ▶️ Initialisation de Flask
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 Mo

# 📁 Dossiers de travail
BASE_DIR = os.path.dirname(__file__)
OUTPUT_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "Generated_Files")
TEXT_FOLDER = os.path.join(BASE_DIR, "text_inputs")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(TEXT_FOLDER, exist_ok=True)

# 🌐 À mettre à jour si l’URL ngrok change
NGROK_URL = "https://d097-195-135-2-115.ngrok-free.app"

@app.route('/')
def home():
    return "🚀 Serveur Flask opérationnel !"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Génère un document PDF ou DOCX depuis les données reçues"""
    data = request.get_json(force=True)
    print("📥 Données reçues :", data)

    if not data:
        return jsonify({"status": "error", "message": "Aucune donnée reçue"}), 400

    format_type = data.get("format", "PDF").upper()
    titre = data.get("titre", "Document généré par Chatbot")
    date = data.get("date", datetime.now().strftime("%d/%m/%Y"))
    contenu = ""

    # 📂 Soit le contenu vient d’un fichier .txt
    if "contenu_file" in data:
        filename = data["contenu_file"]
        text_path = os.path.join(TEXT_FOLDER, filename)
        if not os.path.exists(text_path):
            return jsonify({"status": "error", "message": f"Fichier introuvable : {filename}"}), 404
        with open(text_path, "r", encoding="utf-8") as f:
            contenu = f.read()
    # 🧾 Soit le contenu est fourni directement
    elif "contenu" in data:
        contenu = data["contenu"]
    else:
        return jsonify({"status": "error", "message": "Aucun contenu fourni"}), 400

    # 🕒 Ajout horodatage
    contenu += f"\n\n(Généré le {datetime.now().strftime('%d/%m/%Y %H:%M:%S')})"

    # 📄 Génération du document
    output_file = os.path.join(OUTPUT_FOLDER, f"document_chatbot.{format_type.lower()}")

    try:
        if format_type == "PDF":
            generate_pdf(titre, date, contenu, output_file)
        elif format_type == "DOCX":
            generate_docx(titre, date, contenu, output_file)
        else:
            return jsonify({"status": "error", "message": "Format non supporté"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erreur lors de la génération : {str(e)}"}), 500

    # 🔗 Lien de retour
    return jsonify({
        "status": "success",
        "document_url": f"{NGROK_URL}/download?file={os.path.basename(output_file)}"
    })

@app.route('/webhook', methods=['GET'])
def webhook_info():
    return "✅ Endpoint /webhook en ligne. Envoie une requête POST pour générer un document."

@app.route('/download', methods=['GET'])
def download():
    file_name = request.args.get('file')
    file_path = os.path.join(OUTPUT_FOLDER, file_name)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"status": "error", "message": "Fichier introuvable"}), 404

# ▶️ Lancement de l'application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
