import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Weather Analysis", page_icon="📊")


st.markdown("# 🚧 Page Under Construction 🚧")
st.write(
    """I am currently working on analyzing the weather data collected from 
    various cities across France. This section will soon be available with 
    accuracy metrics and other valuable insights.  
    Stay tuned! ⏳"""
)


# Titre de la page
st.markdown("""<h1 style='text-align: center; font-size: 7em;'>
            The project
            </h1>""", unsafe_allow_html=True)

st.write(
    """The France Adventure Planner project is based on collecting and analysing weather 
    and hotel data to help Parisians choose the best weekend destination based on 
    real-time weather conditions. """
)

st.markdown("#### Explanation of the Data for This Analysis")
st.write("""
To evaluate the reliability of weather forecasts across France, I collected 
meteorological data for 50 cities from a larger dataset of 250 locations. The data 
was recorded over a two-month period from December 5, 2024, to February 7, 2025, 
and was structured into 5 separate files, each corresponding to a different forecast 
horizon:

- **Jour 1** → Weather forecast for the next day
- **Jour 2** → Weather forecast for the second day ahead
- **Jour 3** → Weather forecast for the third day ahead
- **Jour 4** → Weather forecast for the fourth day ahead
- **Jour 5** → Weather forecast for the fifth day ahead
    
This segmentation allows for a detailed comparison of forecast accuracy over time,
helping to identify which locations have the most reliable weather predictions in 
France.
""")

st.markdown("""
    France Adventure Planner is more than just a weather-based trip planner. It is a fully 
    automated application that not only provides real-time insights for users but also 
    stores data for advanced analysis. By leveraging data collection, processing, and 
    visualization, the project offers both immediate usability and long-term analytical 
    value.
""")

st.markdown("### - Data Sources")
st.markdown("""
- **OpenWeatherMap API **: Provides detailed weather forecasts (temperature, weather conditions, rain probability, etc)
- **Nominatim API**: Retrieves Latitude & Longitude coordinates for selected cities.
- **Scrapy (Web Scraping)**: Extracts hotel recommendations from Booking.com.
- **GitHub Actions**: Automates the script execution to update data daily.
""")

st.markdown("#### - Data collection flow")
# Affiche l'image
st.image("Assets/DataFlow.png", use_container_width=False, width=600)


# Définition des chemins des fichiers
file_paths = {
    "jour1": "Analyse_Bloc_6_CDSD/forecasts/weather_data_forecast_1day.csv",
    "jour2": "Analyse_Bloc_6_CDSD/forecasts/weather_data_forecast_2day.csv",
    "jour3": "Analyse_Bloc_6_CDSD/forecasts/weather_data_forecast_3day.csv",
    "jour4": "Analyse_Bloc_6_CDSD/forecasts/weather_data_forecast_4day.csv",
    "jour5": "Analyse_Bloc_6_CDSD/forecasts/weather_data_forecast_5day.csv",
}

# Charger chaque fichier en DataFrame
dfs = {day: pd.read_csv(path) for day, path in file_paths.items()}

# Liste des colonnes à conserver une seule fois
columns_to_keep_once = ["Ville", "Latitude", "Longitude", "Date"]

# Séparer les colonnes uniques et les données spécifiques aux jours
df_base = dfs["jour1"][columns_to_keep_once].copy()  # On garde ces colonnes depuis le premier fichier

# Supprimer ces colonnes des autres fichiers avant la fusion et ajouter des suffixes
for day in dfs:
    dfs[day] = dfs[day].drop(columns=columns_to_keep_once, errors="ignore").add_suffix(f"_{day}")

# Fusionner les fichiers sans les colonnes redondantes
all_data = pd.concat([df_base] + list(dfs.values()), axis=1)

# Définir les bornes de température
min_temp = all_data["Temp_Avg_jour1"].min()
max_temp = all_data["Temp_Avg_jour1"].max()

fig = px.density_mapbox(
    all_data,
    lat="Latitude_jour1",
    lon="Longitude_jour1",
    z="Temp_Avg_jour1",  # Influence des données de Temp_Avg
    mapbox_style="open-street-map",
    zoom=3.5,
    radius=7,
    color_continuous_scale="thermal",
    center={"lat": 46.603354, "lon": 1.888334},
    labels={"Temp_Avg_jour1": "Average temperature (°C)"},
    range_color=[min_temp, max_temp]  # Échelle de couleur fixe
)

# Affichage
st.plotly_chart(fig, use_container_width=True)







