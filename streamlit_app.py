import streamlit as st
import requests

# ✅ Lien vers l'API locale Flask
API_URL = "https://a684-195-135-2-115.ngrok-free.app/generer"


st.title("📄 Générateur de Documents PDF & DOCX")
st.write("Remplissez les informations ci-dessous pour générer un document.")

# Champs utilisateur
titre = st.text_input("📌 Titre du document", "Mon Document")
date = st.date_input("📅 Date du document")
contenu = st.text_area("📝 Contenu", "Écrivez ici le contenu du document...")
format_choice = st.selectbox("📄 Format du document", ["PDF", "DOCX"])

if st.button("🚀 Générer le document"):
    if titre and contenu:
        data = {
            "format": format_choice,
            "titre": titre,
            "date": str(date),
            "contenu": contenu
        }

        try:
            # Envoi de la requête POST vers l'API
            response = requests.post(API_URL, json=data)

            if response.status_code == 200:
                response_json = response.json()
                key = format_choice.lower()
                chemin_telechargement = response_json.get(key)

                if not chemin_telechargement:
                    st.error("❌ Aucun lien de téléchargement retourné par l'API.")
                else:
                    # Récupération du document généré via un GET
                    document_url = "http://localhost:5000" + chemin_telechargement
                    fichier = requests.get(document_url)

                    if fichier.status_code == 200:
                        st.success("✅ Document généré avec succès !")
                        st.download_button(
                            "📥 Télécharger le document",
                            data=fichier.content,
                            file_name=f"{titre.replace(' ', '_')}.{format_choice.lower()}",
                            mime="application/octet-stream"
                        )
                    else:
                        st.error("❌ Erreur lors du téléchargement du fichier.")
            else:
                erreur = response.json().get("error", "Erreur inconnue.")
                st.error(f"❌ Erreur {response.status_code} : {erreur}")

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Erreur de connexion à l'API : {e}")
    else:
        st.warning("⚠️ Veuillez remplir tous les champs avant de générer le document.")

st.markdown("---")
st.markdown("🖥️ Application connectée à une API Flask locale.")
