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

# Afficher les 5 premières lignes
st.write(all_data.head())



