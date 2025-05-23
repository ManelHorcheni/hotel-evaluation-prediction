import pandas as pd
from ydata_profiling import ProfileReport

class HotelDataProfiler:
    def __init__(self, input_file='data/hotels_prepares.csv', output_file='reports/rapport_profiling.html'):
        self.input_file = input_file
        self.output_file = output_file
        self.df = None

    def load_data(self):
        print("📂 Chargement des données...")
        self.df = pd.read_csv(self.input_file)
        print(f"✅ Données chargées avec {self.df.shape[0]} lignes et {self.df.shape[1]} colonnes.")

    def generate_report(self):
        print("📊 Génération du rapport de profiling...")
        profile = ProfileReport(self.df, title="Profiling des Hôtels", explorative=True)
        profile.to_file(self.output_file)
        print(f"✅ Rapport généré et sauvegardé dans '{self.output_file}'.")

    def run(self):
        self.load_data()
        self.generate_report()

# Exemple d'utilisation
if __name__ == '__main__':
    profiler = HotelDataProfiler()
    profiler.run()