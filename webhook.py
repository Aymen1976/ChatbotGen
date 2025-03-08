from flask import Flask, request, jsonify, send_file
import subprocess
import os
import json

app = Flask(__name__)

# Dossier où les fichiers seront stockés
OUTPUT_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop")

@app.route('/generate', methods=['POST'])
def generate():
    """ Générer un document basé sur les données reçues en JSON """
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Aucune donnée reçue"}), 400

    # Sauvegarde les données dans un fichier temporaire
    temp_file = os.path.join(OUTPUT_FOLDER, 'sample_input_temp.json')
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    # Exécute le script de génération de document
    try:
        subprocess.run(['python', 'generate_document.py', temp_file], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
    # Détermine le fichier de sortie
    output_file = "document_chatbot.pdf" if data.get("format", "DOCX").upper() == "PDF" else "document_chatbot.docx"
    output_path = os.path.join(OUTPUT_FOLDER, output_file)

    # Vérifie si le fichier a bien été généré
    if os.path.exists(output_path):
        # Retourne un lien de téléchargement au lieu du fichier brut
        return jsonify({
            "status": "success",
            "document_url": f"http://localhost:5000/download?file={output_file}"
        })
    else:
        return jsonify({"status": "error", "message": "Erreur lors de la génération du document"}), 500

@app.route('/download', methods=['GET'])
def download():
    """ Permet de télécharger le fichier généré """
    file_name = request.args.get('file')
    file_path = os.path.join(OUTPUT_FOLDER, file_name)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"status": "error", "message": "Fichier introuvable"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
