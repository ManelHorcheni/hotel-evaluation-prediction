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
        self.predictor.train_classifier()

        # ✅ Vérifier que le modèle a été instancié
        self.assertIsNotNone(self.predictor.model_cls)

        # ✅ Vérifier que le modèle peut faire une prédiction
        sample = self.predictor.X.iloc[[0]]  # une ligne de test
        prediction = self.predictor.model_cls.predict(sample)
        self.assertTrue(len(prediction) == 1)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)