import streamlit as st
import pandas as pd
from hotel_star_predictor import HotelStarPredictor

# Initialisation du prédicteur et chargement des modèles
@st.cache_resource
def load_predictor():
    predictor = HotelStarPredictor()
    # Charger les modèles et l'encodeur sauvegardés
    import joblib
    predictor.model_reg = joblib.load(predictor.model_reg_file)
    predictor.encoder = joblib.load(predictor.encoder_file)
    return predictor

predictor = load_predictor()

st.title("Prédiction de l'évaluation d'un hôtel")

# Inputs utilisateur pour chaque feature (exemple avec des features types)
capacite = st.number_input("Capacité (nombre de chambres)", min_value=1, max_value=1000, value=100)
prix_moyen = st.number_input("Prix moyen par nuit (€)", min_value=0.0, max_value=1000.0, value=100.0)
classe_service = st.selectbox("Classe de service", options=["Économique", "Moyenne", "Luxe"])
# Localisation fixe "Hammamet"
localisation = "Hammamet"
nom_hotel = ""  # Vide car tu ne veux pas le nom

# Construire un dict pour toutes les colonnes nécessaires selon ton dataset
data_input = {
    'Emplacement': [localisation],        # Colonne attendue
    'Lieu': [localisation],               # Si utile aussi
    'Nom de l\'hôtel': [nom_hotel],      # Vide pour éviter la prise en compte
    'Capacite': [capacite],
    'Prix_moyen': [prix_moyen],
    'Classe_service': [classe_service],

}

df_input = pd.DataFrame(data_input)

# Bouton pour lancer la prédiction
if st.button("Prédire"):
    try:
        # Préparer l'entrée et appeler la méthode predict de la classe
        prediction = predictor.predict(df_input)
        st.success(f"Prédiction du nombre d'étoiles : {prediction[0]:.1f}")
    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")
