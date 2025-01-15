import asyncio
import os
import logging
import requests
import pandas as pd
from datetime import datetime, timedelta
import scrapy # type: ignore
from scrapy.crawler import CrawlerProcess # type: ignore
import time
from dotenv import load_dotenv # type: ignore
import os


# Forcer SelectorEventLoop sur Windows
if asyncio.get_event_loop_policy().__class__.__name__ == 'WindowsProactorEventLoopPolicy':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# API Key OpenWeatherMap
load_dotenv()
api_key = os.getenv("API_KEY")

# Liste des villes
villes = [
    # Analyse Météo
    "Paris",  "Lyon", "Toulouse",    "Nantes", "Strasbourg", "Bordeaux", "Lille", 
    "Rennes", "Reims", "Saint-Étienne", "Toulon", "Dijon", "Angers", "Nîmes", 
    "Villeurbanne", "Le Mans", "Clermont-Ferrand", "Brest", "Aix-en-Provence", 
    "Amiens", "Limoges", "Annecy", "Perpignan", "Caen", "Metz", "Besançon", 
    "Orléans", "Rouen", "Avignon", "Pau", "Poitiers", "Mulhouse", "Colmar", 
    "Chambéry", "Lourdes", "Arles", "Carcassonne", "Albi", "Ajaccio",
    #Alpes
    #Les Ecrins
    "Bourg d'Oisans", "Le Périer", "La Chapelle-en-Valgaudémar", "Vallouise",
    "Ailefroide", "Monêtier-les-Bains", "La Grave", "Saint-Christophe-en-Oisans",
    #Mt-Blanc
    "Chamonix", "Les Houches", "Saint-Gervais-les-Bains", 
    "Servoz", "Vallorcine", "Argentière", "Combloux", "Megève", 
    "Les Contamines-Montjoie", "Cordon", "Domancy", "Demi-Quartier", 
    "Praz-sur-Arly", "Sixt-Fer-à-Cheval", 
    #Vanoise
    "Val-d'Isère", "Tignes", "Pralognan-la-Vanoise", "Termignon", "Modane", 
    "Bonneval-sur-Arc", "Aussois", "Lanslebourg-Mont-Cenis", "Bessans",
    #Beaufortain
    "Beaufort", "Arêches", "Les Saisies", "Hauteluce", "Villard-sur-Doron", 
    "Queige",
    #Chartreuse
    "Saint-Pierre-de-Chartreuse", "Grenoble", "Le Sappey-en-Chartreuse",
    "Saint-Laurent-du-Pont", "Entremont-le-Vieux",
    #Mercantour
    "Saint-Martin-Vésubie", "Isola", "Barcelonnette", "Tende", "Valdeblore",
    "La Brigue", "Breil-sur-Roya", "Rimplas",
    #Queyras
    "Saint-Véran", "Abriès", "Ceillac", "Guillestre", "Molines-en-Queyras", 
    "Château-Ville-Vieille", "Aiguilles",
    #Maurienne
    "Saint-Jean-de-Maurienne", "Valloire", "Lanslebourg-Mont-Cenis", "Termignon", 
    "Albiez-Montrond", "Aussois", "Bessans", "Saint-Sorlin-d'Arves", 
    "Saint-Colomban-des-Villards",
    #Pyrénées
    #Pyrénées Occidentales (Ouest)
    "Gourette", "Eaux-Bonnes", "Artouste", "Arudy", "Oloron-Sainte-Marie", 
    "Portet-d'Aspet",
    #Pyrénées Centrales
    "Saint-Lary-Soulan", "Luz-Saint-Sauveur", "Cauterets", "Gavarnie", "Barèges", 
    "Bagnères-de-Bigorre", "Piau-Engaly", "Campan", "Ax-les-Thermes", 
    "Luchon (Bagnères-de-Luchon)", "Peyragudes",
    #Pyrénées Orientales (Est)
    "Font-Romeu", "Les Angles", "Mont-Louis", "Villefranche-de-Conflent", 
    "Prats-de-Mollo-la-Preste",
    #Jura
    "Les Rousses", "Morbier", "Saint-Claude", "Lons-le-Saunier", "Arbois", 
    "Baume-les-Messieurs", "Salins-les-Bains", "Métabief", "Clairvaux-les-Lacs", 
    "Lamoura", "Château-Chalon", "Nantua",   
    #Mediterranée
    "Nice", "Cannes", "Antibes", "Saint-Tropez", "Menton", "Juan-les-Pins", 
    "Marseille", "Cassis", "Bandol", "Hyères", "Sanary-sur-Mer", "Montpellier", 
    "Sète", "Agde", "Cap d’Agde", "Gruissan", "Narbonne", "Palavas-les-Flots", 
    "Collioure", "Port-Vendres", "Banyuls-sur-Mer", "Argelès-sur-Mer",
    #Littoral Atlantique
    "Hendaye", "Saint-Jean-de-Luz", "Biarritz", "Anglet", "Bayonne", "Hossegor", 
    "Capbreton", "Seignosse", "Biscarrosse", "Mimizan", "Arcachon", 
    "Lège-Cap-Ferret", "Lacanau", "Soulac-sur-Mer", "Les Sables-d'Olonne", 
    "Saint-Jean-de-Monts", "Saint-Gilles-Croix-de-Vie", "La Tranche-sur-Mer", 
    "Île de Noirmoutier", "Île d'Yeu", "La Rochelle", "Île de Ré", "Île d'Oléron", 
    "Royan", "Châtelaillon-Plage", "Rochefort", 
    #Bretagne/Normandie
    "Vannes", "Lorient", "Carnac", "Quiberon", "La Baule", "Pornic", "Saint-Nazaire",
    "Pornic", "Préfailles", "Saint-Brévin-les-Pins", "Saint-Malo", "Dinard", 
    "Cancale", "Deauville", "Trouville-sur-Mer", "Cabourg", "Honfleur", "Étretat", 
    "Fécamp", "Dieppe", "Le Havre",
    #Littoral de la Manche
    "Calais", "Boulogne-sur-Mer", "Wimereux", "Wissant", "Le Touquet", 
    "Berck-sur-Mer", "Saint-Valery-sur-Somme", "Le Crotoy", "Cayeux-sur-Mer", 
    "Mers-les-Bains"
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

# Créer une colonne "Day_Time"
def time_of_the_day(dt):
    hour = dt.hour
    if 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    elif 18 <= hour < 22:
        return "Evening"
    else:
        return "Night"

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
                    date_hour = pd.to_datetime(day["dt"],unit="s")
                    meteo_resultats.append({
                        "Ville": ville,
                        "Latitude": lat,
                        "Longitude": lon,
                        "Date": date_hour.strftime('%Y-%m-%d'),
                        "Hour": date_hour.hour,
                        "Day_Time": time_of_the_day(date_hour),
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
# Add the column Run_Date
run_date = datetime.now().strftime("%Y-%m-%d")
df_meteo["Run_Date"] = run_date
# convert the "Date" in a datetime format
df_meteo["Date"] = pd.to_datetime(df_meteo["Date"])



# SCRAPING

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

# URL SNCF personnalisé par ville
train_base_url = "https://www.sncf-connect.com/app/home/search/od?originLabel=Paris&originId=RESARAIL_STA_8768600&destinationLabel={}&destinationId=RESARAIL_STA_8774678&outwardDateTime=2025-01-15T08:30:00&directTrains=true"

for _, row in df_meteo.iterrows():
    ville = row["Ville"]
    hotels = next((h["hotels"] for h in hotel_results if h["city"] == ville), [])
    combined_row = row.to_dict()
    for i, hotel in enumerate(hotels):
        combined_row[f"Hotel_{i+1}_Name"] = hotel.get("hotel_name", "N/A")
        combined_row[f"Hotel_{i+1}_Link"] = hotel.get("link", "N/A")
    
    combined_row["Train"] = train_base_url.format(ville.replace(" ", "%20"))
    combined_results.append(combined_row)

# Convertir en DataFrame
df_combined = pd.DataFrame(combined_results)

# Sauvegarder les données combinées dans un fichier principal
output_file = "final_results.csv"
df_combined.to_csv(output_file, index=False, encoding="utf-8")
print(f"Les résultats finaux ont été enregistrés dans {output_file}.")



# Charger les données météo consolidées
df_meteo = pd.read_csv("final_results.csv")
df_meteo["Date"] = pd.to_datetime(df_meteo["Date"])

# Chemin de sauvegarde des fichiers forecasts
output_folder = "forecasts"
os.makedirs(output_folder, exist_ok=True)

# Liste des villes fichiers forecasts
cities_to_split = [
    "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg",
    "Montpellier", "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre",
    "Saint-Étienne", "Toulon", "Grenoble", "Dijon", "Angers", "Nîmes",
    "Villeurbanne", "Le Mans", "Clermont-Ferrand", "Brest", "Aix-en-Provence",
    "Amiens", "Limoges", "Annecy", "Perpignan", "Boulogne-sur-Mer", "Biarritz",
    "Caen", "Metz", "Besançon", "Orléans", "Rouen", "Avignon", "Pau",
    "Poitiers", "Mulhouse", "La Rochelle", "Bayonne", "Colmar", "Chambéry",
    "Lourdes", "Saint-Malo", "Chamonix", "Arles", "Carcassonne",
    "Albi", "Ajaccio"
]

# Liste des colonnes fichiers forecasts
columns_to_save = [
    "Ville", "Latitude", "Longitude", "Date", "Hour",
    "Temp_Max", "Temp_Min", "Humidity", "Weather", "Rain_Probability",
    "Weather_Score", "Temp_Avg", "Run_Date"
]

# Sauvegarder les prévisions d'un jour spécifique
def save_forecast_append(df, day_offset, output_folder, cities, columns):
    target_date = (datetime.now() + timedelta(days=day_offset)).date()
    # Filtrer les données par date, ville et colonnes
    filtered_data = df[(df["Date"].dt.date == target_date) & (df["Ville"].isin(cities))]
    filtered_data = filtered_data[columns]
     
    if not filtered_data.empty:
        output_file = os.path.join(output_folder, f"weather_data_forecast_{day_offset}day.csv")
        
        if os.path.exists(output_file):
            # Charger les données existantes
            existing_data = pd.read_csv(output_file)
            combined_data = pd.concat([existing_data, filtered_data], ignore_index=True)
        else:            
            combined_data = filtered_data
        
        # Sauvegarder les données combinées
        combined_data.to_csv(output_file, index=False, encoding="utf-8")
        print(f"Données ajoutées à {output_file}.")
    else:
        print(f"Aucune donnée disponible pour la date {target_date}.")

# Sauvegarder les 5 jours de prévision pour les 50 villes
for day in range(1, 6):
    save_forecast_append(df_meteo, day, output_folder, cities_to_split, columns_to_save)

# Sauvegarder final_results.csv
df_meteo.to_csv("final_results.csv", index=False, encoding="utf-8")
print("final_results.csv sauvegardé.")