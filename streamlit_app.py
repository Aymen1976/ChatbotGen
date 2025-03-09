import streamlit as st
import requests
import json

API_URL = "http://localhost:5000/generate"

st.title("📄 Générateur de Documents PDF & DOCX")
st.write("Remplissez les informations ci-dessous pour générer un document.")

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
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                document_url = response.json().get("document_url")
                st.success("✅ Document généré avec succès !")
                with st.spinner("Préparation du téléchargement..."):
                    st.download_button("📥 Télécharger le document", document_url, file_name=f"document.{format_choice.lower()}")
            else:
                st.error(f"❌ Erreur {response.status_code}: {response.json().get('message', 'Erreur inconnue')}")
        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Erreur de connexion à l'API : {e}")
    else:
        st.warning("⚠️ Veuillez remplir tous les champs !")

st.write("---")
st.write("🚀 **Déployé avec Streamlit**")
