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

# Exemple de treks
treks = {
    "Northern Alps (Mont-Blanc)": ["Chamonix", "Les Houches", 
                                   "Saint-Gervais-les-Bains", "Servoz", "Vallorcine", 
                                   "Argentière", "Combloux", "Megève", 
                                   "Les Contamines-Montjoie", "Cordon", "Domancy", 
                                   "Demi-Quartier", "Praz-sur-Arly", 
                                   "Sixt-Fer-à-Cheval"],
    "Central Alps (Vanoise, Écrins, Beaufortain)": ["Bourg d'Oisans", "Le Périer", 
                                                        "La Chapelle-en-Valgaudémar", "Vallouise", 
                                                        "Ailefroide", "Monêtier-les-Bains", "La Grave", 
                                                        "Saint-Christophe-en-Oisans", "Val-d'Isère", 
                                                        "Tignes", "Pralognan-la-Vanoise", "Termignon", 
                                                        "Modane", "Bonneval-sur-Arc", "Aussois", 
                                                        "Lanslebourg-Mont-Cenis", "Bessans", "Beaufort", 
                                                        "Arêches", "Les Saisies", "Hauteluce", 
                                                        "Villard-sur-Doron", "Queige", 
                                                        "Saint-Pierre-de-Chartreuse", "Grenoble", 
                                                        "Le Sappey-en-Chartreuse", "Saint-Laurent-du-Pont", 
                                                        "Entremont-le-Vieux"],
    "Southern Alps (Écrins, Queyras, Mercantour)": ["Saint-Martin-Vésubie", "Isola", "Barcelonnette", 
                                                   "Tende", "Valdeblore", "La Brigue", "Breil-sur-Roya", 
                                                   "Rimplas", "Saint-Véran", "Abriès", "Ceillac", "Guillestre", 
                                                   "Molines-en-Queyras", "Château-Ville-Vieille", "Aiguilles", 
                                                   "Saint-Jean-de-Maurienne", "Valloire", "Lanslebourg-Mont-Cenis", 
                                                   "Termignon", "Albiez-Montrond", "Aussois", "Bessans", 
                                                   "Saint-Sorlin-d'Arves", "Saint-Colomban-des-Villards"],
    "Western Pyrenees": ["Gourette", "Eaux-Bonnes", "Artouste", "Arudy", 
                                      "Oloron-Sainte-Marie"],
    "Central Pyrenees": ["Saint-Lary-Soulan", "Luz-Saint-Sauveur", "Cauterets", 
                           "Gavarnie", "Barèges", "Bagnères-de-Bigorre", 
                           "Piau-Engaly", "Campan", "Les Angles", "Portet-d'Aspet",
                           "Luchon (Bagnères-de-Luchon)", "Peyragudes"],
    "Eastern Pyrenees": ["Font-Romeu", "Mont-Louis", 
                                  "Villefranche-de-Conflent", "Ax-les-Thermes",
                                  "Prats-de-Mollo-la-Preste"],
    "Jura": ["Les Rousses", "Morbier", "Saint-Claude", "Lons-le-Saunier", 
             "Arbois", "Baume-les-Messieurs", "Salins-les-Bains", "Métabief", 
             "Clairvaux-les-Lacs", "Lamoura", "Château-Chalon", "Nantua"]
}

# Titre
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

# Carte
if not df_filtered.empty:
        
    # Centrer la carte sur les coordonnées
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
        zoom=6,  
        radius=7,
        center={"lat": center_lat, "lon": center_lon},
        color_continuous_scale="Plasma",
        hover_data=["Temp_Max", "Temp_Min", "Humidity", "Weather"]
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Titre
st.title("Explore Weather and Links 🏙️🚆")
# Filtrer les villes en fonction du trek
selected_cities = treks[chosen_trek]

# Bouton pour afficher les informations d'une ville
selected_city = st.selectbox("Choose a city :", selected_cities)

# Filtrer les données pour la ville sélectionnée
city_data = df[df["Ville"] == selected_city]
if not city_data.empty:
    # Regrouper les données par jour
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

    # Afficher tableau
    st.markdown(f"### Forecast for **{selected_city}**")
    st.dataframe(city_grouped[[
        "Date", "Temp_Max", "Temp_Min", "Temp_Avg", "Humidity", "Rain_Probability", "Weather"
    ]])

    # Afficher le lien du train
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
        # Regrouper par Date et Day_Time
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
    "Weather": lambda x: x.mode()[0]  # Météo la plus fréquente pour chaque période
})

# Avoir "Day_Time" comme colonnes
pivot_table = grouped_data.pivot(index="Date", columns="Day_Time", values="Weather")

