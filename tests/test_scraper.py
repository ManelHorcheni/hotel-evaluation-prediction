import unittest
from scraper import HotelScraper  # adapte selon ton nom de classe/fonction

class TestHotelScraper(unittest.TestCase):

    def setUp(self):
        # Liste de liens pour initialiser le scraper (exemple fictif)
        self.test_links = [
            "https://tn.tunisiebooking.com/detail_hotel_1/",
            "https://tn.tunisiebooking.com/detail_hotel_2/"
        ]
        self.scraper = HotelScraper(self.test_links)

    def test_scrape_returns_data(self):
        data = self.scraper.scrape()
        self.assertIsNotNone(data)
        self.assertTrue(len(data) > 0)

   
        
if __name__ == '__main__':
    unittest.main()
