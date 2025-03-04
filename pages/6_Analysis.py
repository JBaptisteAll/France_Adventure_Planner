import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Weather Analysis", page_icon="📊")


# Titre de la page
st.markdown("""<h1 style='text-align: center; font-size: 7em;'>
             Data Analysis 
            </h1>""", unsafe_allow_html=True)

st.write(
    """The France Adventure Planner project is based on collecting and analysing weather 
    and hotel data to help Parisians choose the best weekend destination based on 
    real-time weather conditions. """
)

st.write(
    """Explanation of the Data for This Analysis
To evaluate the reliability of weather forecasts across France, I collected meteorological 
data for 50 cities from a larger dataset of 250 locations. The data was recorded over 
a two-month period from December 5, 2024, to February 7, 2025, and was structured into 
5 separate files, each corresponding to a different forecast horizon:
- **Jour 1** → Weather forecast for the next day
- **Jour 2** → Weather forecast for two days ahead
- **Jour 3** → Weather forecast for three days ahead
- **Jour 4** → Weather forecast for four days ahead
- **Jour 5** → Weather forecast for five days ahead

This segmentation allows for a detailed comparison of forecast accuracy over time, 
helping to identify which locations have the most reliable weather predictions in France.
"""
)

st.markdown("#### - Data Sources")
st.markdown("""
- **OpenWeatherMap API **: Provides detailed weather forecasts (temperature, weather conditions, rain probability, etc)
- **Nominatim API**: Retrieves Latitude & Longitude coordinates for selected cities.
- **Scrapy (Web Scraping)**: Extracts hotel recommendations from Booking.com.
- **GitHub Actions**: Automates the script execution to update data daily.
""")

st.markdown("#### - Data collection flow")





# Définition des chemins des fichiers
file_paths = {
    "jour1": "\Analyse_Bloc_6_CDSD\forecasts\weather_data_forecast_1day.csv",
    "jour2": "\Analyse_Bloc_6_CDSD\forecasts\weather_data_forecast_2day.csv",
    "jour3": "\Analyse_Bloc_6_CDSD\forecasts\weather_data_forecast_3day.csv",
    "jour4": "\Analyse_Bloc_6_CDSD\forecasts\weather_data_forecast_4day.csv",
    "jour5": "\Analyse_Bloc_6_CDSD\forecasts\weather_data_forecast_5day.csv",
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



st.markdown("# COMING SOON")
st.write(
    """This page will contain an analysis of the weather data that we have collected
    from the various cities in France. We will be using the data to provide
    accuracy scores for each city."""
)
