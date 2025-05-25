import unittest
import os
import pandas as pd
from scraper import HotelScraper

class TestHotelScraper(unittest.TestCase):

    def setUp(self):
        self.test_links = [
            "https://tn.tunisiebooking.com/detail_hotel_1/",
            "https://tn.tunisiebooking.com/detail_hotel_2/"
        ]
        self.output_file = "data/test_hotels.csv"
        self.scraper = HotelScraper(self.test_links, output_file=self.output_file)

    def test_scrape_creates_csv_file(self):
        self.scraper.scrape()
        self.assertTrue(os.path.exists(self.output_file))  # vérifie que le fichier existe
        self.assertGreater(os.path.getsize(self.output_file), 0)  # et qu'il n'est pas vide

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)  # Nettoyage après test
    
    #Tester les colonnes du CSV
    def test_csv_columns(self):
        self.scraper.scrape()
        df = pd.read_csv(self.output_file)
        expected_cols = ["Nom de l'hôtel", "Lieu", "Emplacement", "Équipements", "Évaluation"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

if __name__ == '__main__':
    unittest.main()
