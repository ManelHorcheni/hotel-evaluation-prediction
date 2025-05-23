#Importations
import requests
import csv
from bs4 import BeautifulSoup

class HotelScraper:
    def __init__(self, hotel_links, output_file='data/hotels.csv'):
        self.hotel_links = hotel_links
        self.output_file = output_file

    def scrape(self):
        with open(self.output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Nom de l\'hôtel', 'Lieu', 'Emplacement', 'Équipements', 'Évaluation'])

            for hotel_url in self.hotel_links:
                print(f"Scraping {hotel_url} ...")
                try:
                    response = requests.get(hotel_url)
                    if response.status_code != 200:
                        print(f"Erreur de chargement pour {hotel_url}")
                        continue

                    soup = BeautifulSoup(response.content, 'html.parser')

                    hotel_name = self.get_hotel_name(soup)
                    lieu = self.get_lieu(soup)
                    emplacement = self.get_emplacement(soup)
                    equipements = self.get_equipements(soup)
                    evaluation = self.get_evaluation(soup)

                    equipements_string = ', '.join(equipements)
                    writer.writerow([hotel_name, lieu, emplacement, equipements_string, evaluation])

                except Exception as e:
                    print(f"Erreur lors du scraping de {hotel_url}: {e}")

        print("✅ Scraping terminé ! Les informations ont été sauvegardées dans 'hotels.csv'.")

    def get_hotel_name(self, soup):
        element = soup.find('h1', {'class': 'h2styles'})
        return element.get_text(strip=True) if element else 'Non trouvé'

    def get_lieu(self, soup):
        element = soup.find('u', {'class': 'adresse_hotel'})
        return element.get_text(strip=True) if element else 'Non trouvé'

    def get_emplacement(self, soup):
        element = soup.find('div', style=lambda value: value and 'Emplacement' in value)
        return element.get_text(strip=True) if element else 'Non trouvé'

    def get_equipements(self, soup):
        equipements = []
        for span in soup.find_all('span'):
            texte = span.get_text(strip=True)
            equipements.append(texte)

        services_recherches = [
            "Chauffage", "Climatisation", "Coffre fort dans la chambre",
            "Salle de bains avec baignoire", "Salle de bains avec douche",
            "WIFI Gratuit dans les locaux communs", "WIFI Gratuit dans la chambre",
            "Bar", "Restaurant (a la carte)", "Restaurant (Buffet)", "Snack-bar",
            "Restaurant", "Piscine"
        ]
        return [e for e in equipements if e in services_recherches]

    def get_evaluation(self, soup):
        element = soup.find('span', class_='span_tripadv')
        return element.get_text(strip=True) if element else 'Non trouvé'


# Exemple d'utilisation :
if __name__ == '__main__':
    hotel_links = [
        'https://tn.tunisiebooking.com/detail_hotel_419/',
        'https://tn.tunisiebooking.com/detail_hotel_25/',
        'https://tn.tunisiebooking.com/detail_hotel_279/',
        'https://tn.tunisiebooking.com/detail_hotel_350/',
        'https://tn.tunisiebooking.com/detail_hotel_36/',
        'https://tn.tunisiebooking.com/detail_hotel_330/',
        'https://tn.tunisiebooking.com/detail_hotel_60/',
        'https://tn.tunisiebooking.com/detail_hotel_302/',
        'https://tn.tunisiebooking.com/detail_hotel_701/',
        'https://tn.tunisiebooking.com/detail_hotel_781/',
        'https://tn.tunisiebooking.com/detail_hotel_255/',
        'https://tn.tunisiebooking.com/detail_hotel_22/',
        'https://tn.tunisiebooking.com/detail_hotel_204/',
        'https://tn.tunisiebooking.com/detail_hotel_597/',
        'https://tn.tunisiebooking.com/detail_hotel_786/',
        'https://tn.tunisiebooking.com/detail_hotel_59/',
        'https://tn.tunisiebooking.com/detail_hotel_819/',
        'https://tn.tunisiebooking.com/detail_hotel_261/',
        'https://tn.tunisiebooking.com/detail_hotel_240/',
        'https://tn.tunisiebooking.com/detail_hotel_23/',
        'https://tn.tunisiebooking.com/detail_hotel_867/',
        'https://tn.tunisiebooking.com/detail_hotel_465/',
        'https://tn.tunisiebooking.com/detail_hotel_370/',
        'https://tn.tunisiebooking.com/detail_hotel_684/',
        'https://tn.tunisiebooking.com/detail_hotel_101/',
        'https://tn.tunisiebooking.com/detail_hotel_41/',
        'https://tn.tunisiebooking.com/detail_hotel_55/',
        'https://tn.tunisiebooking.com/detail_hotel_28/',
        'https://tn.tunisiebooking.com/detail_hotel_235/',
        'https://tn.tunisiebooking.com/detail_hotel_264/',
        'https://tn.tunisiebooking.com/detail_hotel_372/',
        'https://tn.tunisiebooking.com/detail_hotel_94/',
        'https://tn.tunisiebooking.com/detail_hotel_262/',
        'https://tn.tunisiebooking.com/detail_hotel_587/',
        'https://tn.tunisiebooking.com/detail_hotel_396/',
        'https://tn.tunisiebooking.com/detail_hotel_856/',
        'https://tn.tunisiebooking.com/detail_hotel_875/',
        'https://tn.tunisiebooking.com/detail_hotel_417/',
        'https://tn.tunisiebooking.com/detail_hotel_217/',
        'https://tn.tunisiebooking.com/detail_hotel_196/',
        'https://tn.tunisiebooking.com/detail_hotel_800/',
        'https://tn.tunisiebooking.com/detail_hotel_229/',
        'https://tn.tunisiebooking.com/detail_hotel_432/',
        'https://tn.tunisiebooking.com/detail_hotel_501/',
        'https://tn.tunisiebooking.com/detail_hotel_873/',
        'https://tn.tunisiebooking.com/detail_hotel_272/',
        'https://tn.tunisiebooking.com/detail_hotel_923/',
        'https://tn.tunisiebooking.com/detail_hotel_461/',
        'https://tn.tunisiebooking.com/detail_hotel_218/',
        'https://tn.tunisiebooking.com/detail_hotel_257/',
        'https://tn.tunisiebooking.com/detail_hotel_442/',
        'https://tn.tunisiebooking.com/detail_hotel_190/',
        'https://tn.tunisiebooking.com/detail_hotel_382/',
        'https://tn.tunisiebooking.com/detail_hotel_202/'
    ]

    scraper = HotelScraper(hotel_links)
    scraper.scrape()