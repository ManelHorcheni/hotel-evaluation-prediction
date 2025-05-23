import pandas as pd

class HotelDataPreprocessor:
    def __init__(self, input_file='data/hotels.csv', output_file='data/hotels_prepares.csv'):
        self.input_file = input_file
        self.output_file = output_file
        self.df = None
        self.equipements_possible = [
            "Chauffage", "Climatisation", "Coffre fort dans la chambre",
            "Salle de bains avec baignoire", "Salle de bains avec douche",
            "WIFI Gratuit dans les locaux communs", "WIFI Gratuit dans la chambre",
            "Bar", "Restaurant (a la carte)", "Restaurant (Buffet)", "Snack-bar",
            "Restaurant", "Piscine"
        ]

    def load_data(self):
        print("📂 Chargement des données...")
        self.df = pd.read_csv(self.input_file)
        print(f"✅ Données chargées : {self.df.shape[0]} lignes.")

    def clean_data(self):
        print("🧹 Nettoyage des données...")
        self.df.drop_duplicates(inplace=True)
        self.df = self.df[self.df["Nom de l'hôtel"] != 'Non trouvé']
        self.df = self.df[self.df["Lieu"] != 'Non trouvé']
        self.df["Équipements"] = self.df["Équipements"].fillna('')
        print(f"✅ Données nettoyées : {self.df.shape[0]} lignes restantes.")

    def extract_features(self):
        print("🔧 Extraction des caractéristiques...")
        for eq in self.equipements_possible:
            self.df[eq] = self.df["Équipements"].apply(lambda x: 1 if eq in x else 0)
        self.df.drop(columns=["Équipements"], inplace=True)
        print("✅ Caractéristiques extraites.")

    def save_data(self):
        self.df.to_csv(self.output_file, index=False)
        print(f"💾 Données sauvegardées dans '{self.output_file}'")

    def run(self):
        self.load_data()
        self.clean_data()
        self.extract_features()
        self.save_data()
        print("✅ Préparation des données terminée.")

# Exemple d'utilisation
if __name__ == '__main__':
    preprocessor = HotelDataPreprocessor()
    preprocessor.run()