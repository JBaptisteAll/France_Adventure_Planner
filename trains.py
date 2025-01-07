import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

# Données météo fictives
data = {
    "Ville": ["Chamonix", "Les Houches", "Saint-Gervais-les-Bains"],
    "Weather_Score": [9, 8, 7]
}
df_meteo = pd.DataFrame(data)

# Liste des villes
villes = df_meteo["Ville"].tolist()
ville_depart = "Paris"

# Liste pour les résultats de trajet
trajet_results = []

class TrainlineSpider(scrapy.Spider):
    name = "trainline_spider"

    def start_requests(self):
        for ville in villes:
            # Construire une URL valide avec une date et une heure
            url = f"https://www.thetrainline.com/fr/book/results/{ville_depart}/{ville}/2025-01-08-09h00"
            yield scrapy.Request(url=url, callback=self.parse, meta={"destination": ville})

    def parse(self, response):
        destination = response.meta["destination"]
        if response.status == 200:
            trajet_results.append({
                "destination": destination,
                "link": response.url
            })
        else:
            print(f"Erreur lors de la récupération pour {destination}: {response.status}")

# Configurer et exécuter le processus Scrapy
process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'LOG_LEVEL': 'INFO',
})
process.crawl(TrainlineSpider)
process.start(install_signal_handlers=False)

# Intégrer les résultats de trajet avec les données météo
combined_results = []
for _, row in df_meteo.iterrows():
    ville = row["Ville"]
    trajets = next((t["link"] for t in trajet_results if t["destination"] == ville), "N/A")
    combined_row = row.to_dict()
    combined_row["Train_Link"] = trajets
    combined_results.append(combined_row)

# Convertir en DataFrame final et sauvegarder en CSV
df_combined = pd.DataFrame(combined_results)
output_file = "train_results.csv"
df_combined.to_csv(output_file, index=False, encoding="utf-8")
print(f"Les résultats finaux ont été enregistrés dans {output_file}.")
