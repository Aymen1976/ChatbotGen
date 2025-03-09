from flask import Flask, request, jsonify, send_file
import subprocess
import os
import json

app = Flask(__name__)
OUTPUT_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "Generated_Files")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Aucune donnée reçue"}), 400
    
    temp_file = os.path.join(OUTPUT_FOLDER, 'sample_input_temp.json')
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    try:
        subprocess.Popen(['python', 'generate_document.py', temp_file, OUTPUT_FOLDER])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
    output_file = "document_chatbot.pdf" if data.get("format", "DOCX").upper() == "PDF" else "document_chatbot.docx"
    output_path = os.path.join(OUTPUT_FOLDER, output_file)
    
    return jsonify({
        "status": "success",
        "document_url": f"/download?file={output_file}"
    })

@app.route('/download', methods=['GET'])
def download():
    file_name = request.args.get('file')
    file_path = os.path.join(OUTPUT_FOLDER, file_name)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"status": "error", "message": "Fichier introuvable"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
