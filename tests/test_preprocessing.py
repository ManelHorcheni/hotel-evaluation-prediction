import unittest
import pandas as pd
from hotel_star_predictor import HotelStarPredictor  # adapte le nom de fichier

class TestHotelStarPredictor(unittest.TestCase):

    def setUp(self):
        self.predictor = HotelStarPredictor()
        self.predictor.df = pd.DataFrame({
            'Évaluation': ['3', '4', '5'],
            'Lieu': ['Paris', 'Lyon', 'Marseille'],
            'Nom de l\'hôtel': ['A', 'B', 'C'],
            'Climatisation': [1, 0, 1]
        })

    def test_preprocessing_does_not_crash(self):
        try:
            self.predictor.preprocess()
        except Exception as e:
            self.fail(f"Prétraitement a échoué avec une exception : {e}")

    def test_model_training(self):
        self.predictor.preprocess()
        # Correction: Appeler la méthode train_classifier ou train_regressor,
        # car il n'y a pas de méthode train_model dans la classe HotelStarPredictor.
        # Supposons que vous vouliez tester l'entraînement du classificateur.
        self.predictor.train_classifier()
        self.assertIsNotNone(self.predictor.model_cls) # Vérifier le modèle classificateur


if __name__ == '__main__':
    # Modifier l'appel à unittest.main() pour éviter la sortie dans un notebook
    unittest.main(argv=['first-arg-is-ignored'], exit=False)