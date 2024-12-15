import asyncio
import os
import logging
import requests
import pandas as pd
from datetime import datetime, timedelta
import scrapy
from scrapy.crawler import CrawlerProcess
import time


# Forcer SelectorEventLoop sur Windows
if asyncio.get_event_loop_policy().__class__.__name__ == 'WindowsProactorEventLoopPolicy':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# API Key OpenWeatherMap
api_key = "YOUR_API_KEY_HERE"

# Liste des villes
villes = [
    "Bourg d'Oisans", "Le Périer", "La Chapelle-en-Valgaudémar", "Vallouise",
    "Ailefroide", "Monêtier-les-Bains", "La Grave", "Saint-Christophe-en-Oisans"
]

# URL API Nominatim (OpenStreetMap) pour récupérer les coordonnées
nominatim_url = "https://nominatim.openstreetmap.org/search"

# Liste pour stocker les résultats météo
meteo_resultats = []

# Dictionnaire de notation des conditions météo
notations = {
    "clear sky": 600,
    "few clouds": 500,
    "scattered clouds": 400,
    "broken clouds": 300,
    "overcast clouds": 200,    

    "light intensity drizzle": -1,
    "drizzle": -2,
    "heavy intensity drizzle": -3,
    "light intensity drizzle rain": -4,
    "drizzle rain": -5,
    "heavy intensity drizzle rain": -6,
    "shower drizzle": -7,
    "shower rain and drizzle": -8,
    "heavy shower rain and drizzle": -9,    

    "light rain": -10,
    "moderate rain": -20,
    "heavy intensity rain": -30,
    "very heavy rain": -40,
    "extreme rain": -50,
    "freezing rain": -60,
    "light intensity shower rain": -70,
    "shower rain": -80,
    "heavy intensity shower rain": -90,
    "ragged shower rain": -100,

    "thunderstorm with light drizzle": -15,
    "thunderstorm with drizzle": -25,
    "thunderstorm with light rain": -35,
    "thunderstorm with rain": -45,
    "thunderstorm with heavy drizzle": -55,
    "thunderstorm with heavy rain": -65,
    "thunderstorm": -75,
    "heavy thunderstorm": -85,
    "ragged thunderstorm": -95,

    "light snow": -20,
    "snow": -40,
    "heavy snow": -60,
    "sleet": -80,
    "light shower sleet": -100,
    "shower sleet": -120,
    "light rain and snow": -140,
    "rain and snow": -160,
    "light shower snow": -180,
    "shower snow": -200,
    "heavy shower snow": -220,

    "mist": -10,
    "smoke": -20,
    "haze": -30,
    "sand/dust whirls": -40,
    "fog": -50,
    "sand": -60,
    "dust": -70,
    "volcanic ash": -90,
    "squalls": -100,
    "tornado": -400,
}

# Boucle pour récupérer les coordonnées et la météo
for ville in villes:
    params = {"city": ville, "country": "France", "format": "json", "limit": 1}
    headers = {"User-Agent": "NotNecessary"}
    r = requests.get(nominatim_url, params=params, headers=headers)

    if r.status_code == 200:
        data = r.json()
        if data:
            lat, lon = data[0]["lat"], data[0]["lon"]
            weather_url = f"https://api.openweathermap.org/data/2.5/forecast"
            weather_params = {"lat": lat, "lon": lon, "units": "metric", "appid": api_key}
            weather_r = requests.get(weather_url, params=weather_params)

            if weather_r.status_code == 200:
                weather_data = weather_r.json()
                for day in weather_data['list']:
                    meteo_resultats.append({
                        "Ville": ville,
                        "Latitude": lat,
                        "Longitude": lon,
                        "Date": pd.to_datetime(day['dt'], unit='s').strftime('%Y-%m-%d'),
                        "Temp_Max": day['main']['temp_max'],
                        "Temp_Min": day['main']['temp_min'],
                        "Humidity": day['main']['humidity'],
                        "Weather": day['weather'][0]['description'],
                        "Rain_Probability": day['pop']
                    })
    # Attente pour respecter les limites des API
    time.sleep(1)

# Convertir les résultats météo en DataFrame
df_meteo = pd.DataFrame(meteo_resultats)
df_meteo["Weather_Score"] = df_meteo["Weather"].map(notations)
df_meteo["Temp_Avg"] = (df_meteo["Temp_Max"] + df_meteo["Temp_Min"]) / 2

# Liste pour les hôtels
hotel_results = []

class BookingSpider(scrapy.Spider):
    name = "booking_spider"

    def start_requests(self):
        for ville in villes:
            url = f"https://www.booking.com/searchresults.html?ss={ville.replace(' ', '+')}"
            yield scrapy.Request(url=url, callback=self.parse, meta={"city": ville})

    def parse(self, response):
        hotels = response.css("div[data-testid='property-card']")[:5]
        city = response.meta["city"]
        hotel_info = []
        for hotel in hotels:
            hotel_info.append({
                "hotel_name": hotel.css("div[data-testid='title']::text").get(),
                "link": response.urljoin(hotel.css("a[data-testid='title-link']::attr(href)").get())
            })
        hotel_results.append({"city": city, "hotels": hotel_info})

# Configurer et exécuter le processus Scrapy
process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'LOG_LEVEL': logging.INFO,
})
process.crawl(BookingSpider)
process.start(install_signal_handlers=False)

# Intégrer les résultats météo et hôtels
combined_results = []
for _, row in df_meteo.iterrows():
    ville = row["Ville"]
    hotels = next((h["hotels"] for h in hotel_results if h["city"] == ville), [])
    combined_row = row.to_dict()
    for i, hotel in enumerate(hotels):
        combined_row[f"Hotel_{i+1}_Name"] = hotel.get("hotel_name", "N/A")
        combined_row[f"Hotel_{i+1}_Link"] = hotel.get("link", "N/A")
    combined_results.append(combined_row)

# Convertir en DataFrame final et trier par Weather_Score
df_combined = pd.DataFrame(combined_results)
#df_combined = df_combined.sort_values(by="Weather_Score", ascending=False)

# Sauvegarder dans un fichier CSV unique
output_file = "final_results.csv"
df_combined.to_csv(output_file, index=False, encoding="utf-8")
print(f"Les résultats finaux ont été enregistrés dans {output_file}.")
