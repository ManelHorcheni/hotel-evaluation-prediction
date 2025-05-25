import streamlit as st
import pandas as pd
import joblib
from hotel_star_predictor import HotelStarPredictor

# Charger les modèles et l'encodeur
@st.cache_resource
def load_predictor():
    predictor = HotelStarPredictor()
    predictor.model_reg = joblib.load(predictor.model_reg_file)
    predictor.model_cls = joblib.load(predictor.model_cls_file)
    predictor.encoder = joblib.load(predictor.encoder_file)
    predictor.feature_names = joblib.load(predictor.features_file)
    return predictor

predictor = load_predictor()

st.title("⭐ Prédiction du nombre d'étoiles et de l'évaluation d’un hôtel")
#st.write("**Remplissez uniquement les équipements disponibles dans l'hôtel.**")

# === Équipements ===
equipements_possible = [
    "Chauffage", "Climatisation", "Coffre fort dans la chambre",
    "Salle de bains avec baignoire", "Salle de bains avec douche",
    "WIFI Gratuit dans les locaux communs", "WIFI Gratuit dans la chambre",
    "Bar", "Restaurant (a la carte)", "Restaurant (Buffet)", "Snack-bar",
    "Restaurant", "Piscine"
]

equipements_selectionnes = {}
for eq in equipements_possible:
    equipements_selectionnes[eq] = st.checkbox(eq, value=False)

# === Construction de l'entrée ===
data_input = {}
for eq in equipements_possible:
    data_input[eq] = [1 if equipements_selectionnes[eq] else 0]

df_input = pd.DataFrame(data_input)

# === Prédiction ===
if st.button("🔮 Prédire"):
    try:
        # Colonnes numériques uniquement
        cat_cols = []  # Aucun champ catégoriel dans ce cas
        num_cols = df_input.select_dtypes(include='number').columns

        X_processed = df_input.copy()

        # Ajouter colonnes manquantes
        for col in predictor.feature_names:
            if col not in X_processed.columns:
                X_processed[col] = 0

        # Réordonner
        X_processed = X_processed[predictor.feature_names]

        # Prédiction
        pred_reg = predictor.model_reg.predict(X_processed)[0]
        pred_cls = predictor.model_cls.predict(X_processed)[0]

        st.success(f"📐 Régression (évaluations estimées) : **{pred_reg:.2f}**")
        st.info(f"🏷️ Classification (étoiles estimées) : **{pred_cls} étoiles**")

    except Exception as e:
        st.error(f"❌ Erreur lors de la prédiction : {e}")
