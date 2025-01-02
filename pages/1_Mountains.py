import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Trek & Mountains", page_icon="⛰️", layout="wide")

# Fonction pour charger et préparer les données
@st.cache_data
def load_and_prepare_data():
    # Charger les données depuis le fichier CSV
    df = pd.read_csv("final_results.csv")
    
    # Agréger les données par Ville, Date et Moment de la journée
    df_agg = df.groupby(["Ville", "Date", "Latitude", "Longitude"], as_index=False).agg({
        "Temp_Max": "max",
        "Temp_Min": "min",
        "Temp_Avg": "mean",
        "Humidity": "mean",
        "Rain_Probability": "mean",
        "Weather": lambda x: x.mode()[0]
    })
    
    # Arrondir les valeurs numériques
    df_agg["Temp_Max"] = df_agg["Temp_Max"].round(1)
    df_agg["Temp_Min"] = df_agg["Temp_Min"].round(1)
    df_agg["Temp_Avg"] = df_agg["Temp_Avg"].round(1)
    df_agg["Humidity"] = df_agg["Humidity"].round(1)
    df_agg["Rain_Probability"] = df_agg["Rain_Probability"].round(2)
    
    return df

# Charger les données
df = load_and_prepare_data()

# Exemple de treks
treks = {
    "Les Ecrins": ["Bourg d'Oisans", "Le Périer", "La Chapelle-en-Valgaudémar", "Vallouise", "Ailefroide", "Monêtier-les-Bains", "La Grave", "Saint-Christophe-en-Oisans"],
    "Mont-Blanc": ["Chamonix", "Les Houches", "Saint-Gervais-les-Bains"],
    "Pyrénées": ["Aragnouet"],
    "Jura": []
}

# Titre de la page
st.markdown("# Trek & Mountains")
st.markdown("### Select a known trek/hike destination and explore its weather forecasts and nearby accommodations.")

# Sélection de l'itinéraire
chosen_trek = st.selectbox("Choose a Destination :", list(treks.keys()))

# Sélectionner les villes associées à cet itinéraire
selected_cities = treks[chosen_trek]
st.markdown(f"## Forecast for the itinerary **{chosen_trek}**")
st.markdown(f"Cities Involved    : {', '.join(selected_cities)}")

# Filtrer les données pour les villes sélectionnées
df_filtered = df[df["Ville"].isin(selected_cities)]

# Carte interactive
if not df_filtered.empty:
        
    # Centrer la carte sur les coordonnées moyennes des villes sélectionnées
    center_lat = df_filtered["Latitude"].mean()
    center_lon = df_filtered["Longitude"].mean()
    
    # Créer la carte avec Plotly
    fig = px.density_mapbox(
        df_filtered,
        lat="Latitude",
        lon="Longitude",
        z="Temp_Avg",
        mapbox_style="open-street-map",
        animation_frame="Date",
        zoom=6,  # Zoom ajusté
        radius=10,
        center={"lat": center_lat, "lon": center_lon},
        color_continuous_scale="Plasma"
    )
    
    st.plotly_chart(fig, use_container_width=True)

if not df_filtered.empty:
    st.markdown("### Daily Weather Highlights by City")
    for city in selected_cities:
        city_data = df_filtered[df_filtered["Ville"] == city]
        if not city_data.empty:
            # Regrouper par jour
            city_grouped = city_data.groupby(["Date"], as_index=False).agg({
                "Temp_Max": "max",  # Récupérer la température maximale
                "Temp_Min": "min",  # Récupérer la température minimale
                "Temp_Avg": "mean",  # Calculer la moyenne des températures
                "Humidity": "mean",
                "Rain_Probability": "max",
                "Weather": lambda x: x.mode()[0]  # Météo la plus fréquente
            })
            city_grouped["Temp_Max"] = city_grouped["Temp_Max"].round(1)
            city_grouped["Temp_Min"] = city_grouped["Temp_Min"].round(1)
            city_grouped["Temp_Avg"] = city_grouped["Temp_Avg"].round(1)
            city_grouped["Humidity"] = city_grouped["Humidity"].round(1)
            city_grouped["Rain_Probability"] = city_grouped["Rain_Probability"].round(2)
            
            # Afficher les données météo regroupées
            st.markdown(f"### Forecast for **{city}**")
            st.dataframe(city_grouped[[
                "Date", "Temp_Max", "Temp_Min", "Temp_Avg", "Humidity", "Rain_Probability", "Weather"
            ]])
            
            # Ajouter les informations des hôtels
            st.markdown(f"#### Hotels in {city}")
            for i in range(1, 6):  # Suppose qu'il y a jusqu'à 5 hôtels
                hotel_name_col = f"Hotel_{i}_Name"
                hotel_link_col = f"Hotel_{i}_Link"
                
                if hotel_name_col in city_data.columns and hotel_link_col in city_data.columns:
                    hotel_name = city_data[hotel_name_col].iloc[0]
                    hotel_link = city_data[hotel_link_col].iloc[0]
                    
                    if pd.notna(hotel_name) and pd.notna(hotel_link):
                        st.markdown(f"- [{hotel_name}]({hotel_link})")
        else:
            st.markdown(f"No data available for **{city}**.")
else:
    st.write("No data available for this itinerary.")
