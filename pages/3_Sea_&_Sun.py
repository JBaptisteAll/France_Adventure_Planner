import streamlit as st
import pandas as pd
import plotly.express as px


# Fonction pour charger les données
@st.cache_data
def load_and_prepare_data():
    df = pd.read_csv("final_results.csv")
    
    # Agréger les données
    df_agg = df.groupby(["Ville", "Date", "Latitude", "Longitude"], as_index=False).agg({
        "Temp_Max": "max",
        "Temp_Min": "min",
        "Temp_Avg": "mean",
        "Humidity": "mean",
        "Rain_Probability": "mean",
        "Weather": lambda x: x.mode()[0]
    })
    
    # Arrondir
    df_agg["Temp_Max"] = df_agg["Temp_Max"].round(1)
    df_agg["Temp_Min"] = df_agg["Temp_Min"].round(1)
    df_agg["Temp_Avg"] = df_agg["Temp_Avg"].round(1)
    df_agg["Humidity"] = df_agg["Humidity"].round(1)
    df_agg["Rain_Probability"] = df_agg["Rain_Probability"].round(2)
    
    return df

# Charger les données
df = load_and_prepare_data()

regions = {
    "Mediterranean Coast": ["Nice", "Cannes", "Antibes", "Saint-Tropez", "Menton", 
                            "Juan-les-Pins", "Marseille", "Cassis", "Bandol", 
                            "Hyères", "Sanary-sur-Mer", "Montpellier", "Sète", 
                            "Agde", "Cap d’Agde", "Gruissan", "Narbonne", 
                            "Palavas-les-Flots", "Collioure", "Port-Vendres", 
                            "Banyuls-sur-Mer", "Argelès-sur-Mer"],
    "Atlantic Coast": ["Hendaye", "Saint-Jean-de-Luz", "Biarritz", "Anglet", 
                       "Bayonne", "Hossegor", "Capbreton", "Seignosse", 
                       "Biscarrosse", "Mimizan", "Arcachon", "Lège-Cap-Ferret", 
                       "Lacanau", "Soulac-sur-Mer", "Les Sables-d'Olonne", 
                       "Saint-Jean-de-Monts", "Saint-Gilles-Croix-de-Vie", 
                       "La Tranche-sur-Mer", "Île de Noirmoutier", "Île d'Yeu", 
                       "La Rochelle", "Île de Ré", "Île d'Oléron", "Royan", 
                       "Châtelaillon-Plage", "Rochefort"],
    "Bretagne/Normandie": ["Vannes", "Lorient", "Carnac", "Quiberon", "La Baule", 
                           "Pornic", "Saint-Nazaire", "Pornic", "Préfailles", 
                           "Saint-Brévin-les-Pins", "Saint-Malo", "Dinard", 
                           "Cancale", "Deauville", "Trouville-sur-Mer", "Cabourg", 
                           "Honfleur", "Étretat", "Fécamp", "Dieppe", "Le Havre"], 
    "English Channel Coast": ["Calais", "Boulogne-sur-Mer", "Wimereux", "Wissant", 
                              "Le Touquet", "Berck-sur-Mer", "Saint-Valery-sur-Somme", 
                              "Le Crotoy", "Cayeux-sur-Mer", "Mers-les-Bains"]
}

# Titre
st.markdown("# Sea & Sun")
st.markdown("### Choose a coastal region and see weather forecasts and hotel suggestions for famous beach destinations.")

# Sélection de l'itinéraire
chosen_region = st.selectbox("Choose a Coastal Region", list(regions.keys()))

# Sélectionner les villes associées
selected_cities = regions[chosen_region]
st.markdown(f"## Forecast for the itinerary **{chosen_region}**")
st.markdown(f"Cities Involved: {', '.join(selected_cities)}")

# Filtrer les données pour les villes sélectionnées
df_filtered = df[df["Ville"].isin(selected_cities)]

# Carte
if not df_filtered.empty:
        
    # Centrer la carte
    center_lat = df_filtered["Latitude"].mean()
    center_lon = df_filtered["Longitude"].mean()
    
    # Carte
    fig = px.density_mapbox(
        df_filtered,
        lat="Latitude",
        lon="Longitude",
        hover_name="Ville",
        mapbox_style="open-street-map",
        animation_frame="Date",
        z="Temp_Avg",
        zoom=5,
        radius=7,
        center={"lat": center_lat, "lon": center_lon},
        color_continuous_scale="Plasma",
        range_color=[-20, 50],
        hover_data=["Temp_Max", "Temp_Min", "Humidity", "Weather"]
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Titre
st.title("Explore Weather and Links 🏙️🚆")
# Filtrer les villes en fonction de la région
selected_cities = regions[chosen_region]

# Bouton pour afficher les informations d'une seule ville
selected_city = st.selectbox("Choose a city :", selected_cities)

# Filtrer les données pour la ville sélectionnée
city_data = df[df["Ville"] == selected_city]
if not city_data.empty:
    # Regrouper les données
    city_grouped = city_data.groupby(["Date"], as_index=False).agg({
        "Temp_Max": "max",
        "Temp_Min": "min", 
        "Temp_Avg": "mean", 
        "Humidity": "mean",
        "Rain_Probability": "max",
        "Weather": lambda x: x.mode()[0]  
    })

    # Arrondir 
    city_grouped["Temp_Max"] = city_grouped["Temp_Max"].round(1)
    city_grouped["Temp_Min"] = city_grouped["Temp_Min"].round(1)
    city_grouped["Temp_Avg"] = city_grouped["Temp_Avg"].round(1)
    city_grouped["Humidity"] = city_grouped["Humidity"].round(1)
    city_grouped["Rain_Probability"] = city_grouped["Rain_Probability"].round(2)

    # Afficher les prévisions météo
    st.markdown(f"### Forecast for **{selected_city}**")
    st.dataframe(city_grouped[[
        "Date", "Temp_Max", "Temp_Min", "Temp_Avg", "Humidity", "Rain_Probability", "Weather"
    ]])

    # Afficher les trains
    train_link = city_data.iloc[0]["Train"]
    st.markdown(f"[🚄 See Trains for {selected_city}]({train_link})", unsafe_allow_html=True)

    # Afficher les hôtels
    st.markdown(f"#### Hotels in {selected_city}")
    for i in range(1, 6):
        hotel_name_col = f"Hotel_{i}_Name"
        hotel_link_col = f"Hotel_{i}_Link"

        if hotel_name_col in city_data.columns and hotel_link_col in city_data.columns:
            hotel_name = city_data[hotel_name_col].iloc[0]
            hotel_link = city_data[hotel_link_col].iloc[0]

            if pd.notna(hotel_name) and pd.notna(hotel_link):
                st.markdown(f"- [{hotel_name}]({hotel_link})")
else:
    st.markdown(f"No data available for **{selected_city}**.")

st.markdown("## Daily Weather Highlights by City")
for city in selected_cities:
    city_data = df_filtered[df_filtered["Ville"] == city]
    if not city_data.empty:
        # Regrouper 
        grouped_data = df_filtered.groupby(["Date", "Day_Time"], as_index=False).agg({
        "Weather": lambda x: x.mode()[0] 
        })

        # Avoir "Day_Time" comme colonnes
        pivot_table = grouped_data.pivot(index="Date", columns="Day_Time", values="Weather")

        # Réorganiser les colonnes dans l'ordre 
        desired_order = ["Morning", "Afternoon", "Evening", "Night"]
        pivot_table = pivot_table.reindex(columns=desired_order)
                  
        # Afficher 
        st.markdown(f"### **{city}**")
        st.dataframe(pivot_table)

# Regrouper 
grouped_data = df_filtered.groupby(["Date", "Day_Time"], as_index=False).agg({
    "Weather": lambda x: x.mode()[0] 
})

# Avoir "Day_Time" comme colonnes
pivot_table = grouped_data.pivot(index="Date", columns="Day_Time", values="Weather")

