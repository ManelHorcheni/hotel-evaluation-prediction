from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report, accuracy_score, mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np
import joblib
from utils.decorators import timing  # importer le décorateur

class HotelStarPredictor:
    def __init__(self, input_file='data/hotels_prepares.csv', model_cls_file='models/hotel_model.pkl', model_reg_file='models/linear_regression_model.pkl'):
        self.input_file = input_file
        self.model_cls_file = model_cls_file
        self.model_reg_file = model_reg_file
        self.encoder_file = 'models/encoder.pkl'
        self.features_file = 'models/features.pkl'

        self.df = None
        self.X = None
        self.y = None
        self.model_cls = None
        self.model_reg = None
        self.encoder = None
        self.feature_names = None

    def load_data(self):
        print("📂 Chargement des données...")
        self.df = pd.read_csv(self.input_file)
        print(f"✅ {self.df.shape[0]} lignes chargées.")

    @timing
    def preprocess(self):
        print("🔄 Prétraitement...")

        self.df['Évaluation'] = self.df['Évaluation'].replace('Non trouvé', np.nan)
        self.df.dropna(subset=['Évaluation'], inplace=True)
        self.df['Évaluation'] = self.df['Évaluation'].astype(str).str.strip()

        try:
            self.df['Évaluation_float'] = self.df['Évaluation'].astype(float)
        except Exception as e:
            print("❌ Erreur de conversion en float :", e)
            raise

        self.df['Évaluation'] = self.df['Évaluation'].astype('category')

        cols_to_fill = self.df.select_dtypes(include='object').columns.tolist()
        if 'Évaluation' in cols_to_fill:
            cols_to_fill.remove('Évaluation')
        self.df[cols_to_fill] = self.df[cols_to_fill].fillna('')

        self.y = self.df['Évaluation']
        y_float = self.df['Évaluation_float']
        X_raw = self.df.drop(columns=['Évaluation', 'Évaluation_float'])

        cat_cols = X_raw.select_dtypes(include=['object', 'category']).columns
        num_cols = X_raw.select_dtypes(include=np.number).columns

        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        X_encoded = self.encoder.fit_transform(X_raw[cat_cols])
        encoded_names = self.encoder.get_feature_names_out(cat_cols)
        df_encoded = pd.DataFrame(X_encoded, columns=encoded_names, index=X_raw.index)

        self.X = pd.concat([df_encoded, X_raw[num_cols]], axis=1)
        self.feature_names = self.X.columns.tolist()

        self.y_cls = self.y
        self.y_reg = y_float

        print("✅ Prétraitement terminé. X shape:", self.X.shape)

    @timing
    def train_classifier(self):
        print("🎯 Entraînement modèle de classification...")
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y_cls, test_size=0.2, random_state=42)

        self.model_cls = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model_cls.fit(X_train, y_train)

        y_pred = self.model_cls.predict(X_test)
        print(classification_report(y_test, y_pred))
        print(f"✅ Accuracy : {accuracy_score(y_test, y_pred):.2f}")

    def train_regressor(self):
        print("📐 Entraînement modèle de régression linéaire...")
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y_reg, test_size=0.2, random_state=42)

        self.model_reg = LinearRegression()
        self.model_reg.fit(X_train, y_train)

        y_pred = self.model_reg.predict(X_test)

        print(f"📊 MAE : {mean_absolute_error(y_test, y_pred):.2f}")
        print(f"📉 MSE : {mean_squared_error(y_test, y_pred):.2f}")
        print(f"📐 RMSE : {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
        print(f"📈 R² : {r2_score(y_test, y_pred):.2f}")

    def save_models(self):
        print("💾 Sauvegarde des modèles...")
        joblib.dump(self.model_cls, self.model_cls_file)
        joblib.dump(self.model_reg, self.model_reg_file)
        joblib.dump(self.encoder, self.encoder_file)
        joblib.dump(self.feature_names, self.features_file)
        print("✅ Modèles et encodeur sauvegardés.")

    def run(self):
        self.load_data()
        self.preprocess()
        self.train_classifier()
        self.train_regressor()
        self.save_models()

    def predict(self, df_input):
        if self.encoder is None or self.model_reg is None:
            raise ValueError("Modèle ou encodeur non chargé.")
        try:
            self.feature_names = joblib.load(self.features_file)
        except:
            raise ValueError("Fichier contenant les noms des colonnes non trouvé.")

        cat_cols = df_input.select_dtypes(include=['object', 'category']).columns
        num_cols = df_input.select_dtypes(include=np.number).columns

        X_encoded = self.encoder.transform(df_input[cat_cols])
        encoded_names = self.encoder.get_feature_names_out(cat_cols)
        df_encoded = pd.DataFrame(X_encoded, columns=encoded_names, index=df_input.index)

        X_processed = pd.concat([df_encoded, df_input[num_cols]], axis=1)

        for col in self.feature_names:
            if col not in X_processed.columns:
                X_processed[col] = 0
        X_processed = X_processed[self.feature_names]

        return self.model_reg.predict(X_processed)
# Exemple d'utilisation
if __name__ == '__main__':
    predictor = HotelStarPredictor()
    predictor.run()