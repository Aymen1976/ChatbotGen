import streamlit as st
import requests
import json

# 🔗 URL de ton API Flask (Change selon ton URL Ngrok ou ton serveur déployé)
API_URL = "https://1234-5678-abcdef.ngrok-free.app/generate"  # Remplace par ton URL Ngrok si nécessaire

# 🎨 Interface utilisateur
st.title("📄 Générateur de Documents PDF & DOCX")
st.write("Remplissez les informations ci-dessous pour générer un document.")

# 📝 Formulaire de saisie
titre = st.text_input("📌 Titre du document", "Mon Document")
date = st.date_input("📅 Date du document")
contenu = st.text_area("📝 Contenu", "Écrivez ici le contenu du document...")

# 📌 Choix du format (PDF ou DOCX)
format_choice = st.selectbox("📄 Format du document", ["PDF", "DOCX"])

# 🔘 Bouton de génération
if st.button("🚀 Générer le document"):
    if titre and contenu:
        # 🛠️ Préparation des données JSON
        data = {
            "format": format_choice,
            "titre": titre,
            "date": str(date),
            "contenu": contenu
        }

        try:
            # 📤 Envoi de la requête à l'API
            response = requests.post(API_URL, json=data)

            # ✅ Vérification de la réponse
            if response.status_code == 200:
                response_data = response.json()
                st.write(response_data)  # Affiche les données de réponse pour debug

                pdf_url = response_data.get("document_path")
                if pdf_url:
                    st.success(f"✅ {format_choice} généré avec succès !")
                    st.markdown(f"[📥 Télécharger le document]({pdf_url})", unsafe_allow_html=True)
                else:
                    st.error("⚠️ Aucun lien de document retourné par l'API.")
            else:
                st.error(f"❌ Erreur {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("🚨 Impossible de se connecter à l'API. Vérifie que Flask est bien démarré !")
        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Une erreur s'est produite : {e}")

    else:
        st.warning("⚠️ Veuillez remplir tous les champs !")

st.write("---")
st.write("🚀 **Déployé avec Streamlit**")
