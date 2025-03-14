import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import seaborn as sns

st.set_page_config(page_title="Weather Analysis", page_icon="📊")

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


# Extraire la liste des villes uniques dans l'ordre alphabétique
villes_disponibles = all_data["Ville"].unique()
villes_disponibles.sort()

# Sidebar 
with st.sidebar:
    st.markdown(
        """
        <style>
        .sidebar-content {
            font-size: 8px;  /* Réduit la taille du texte */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)

    st.markdown("### 📖 Table of Contents")
    st.markdown("""- [📄 Presentation](#Presentation)""", unsafe_allow_html=True)
    st.markdown("""- [🌤️ Weather Score](#weather-score)""", unsafe_allow_html=True)
    st.markdown("""- [🌡️ Temperature](#temperature)""", unsafe_allow_html=True)
    st.markdown("""- [🌧️ Rain Probability](#rain-probability)""", unsafe_allow_html=True)
    st.markdown("""- [🎯 Weather Accuracy](#accuracy)""", unsafe_allow_html=True)
    
    selected_city = st.selectbox("📍 Select a City:", villes_disponibles)

    # Création d'un lien dynamique vers la section correspondante
    city_anchor = selected_city.lower().replace(" ", "-")
    st.markdown(f"[🔍 View Analysis](#city-{city_anchor})", unsafe_allow_html=True)

    #st.markdown("</div>", unsafe_allow_html=True)  # Fermer le div pour appliquer le CSS



# Titre de la page
st.markdown("""<h1 style='text-align: center; font-size: 7em;'>
            The project
            </h1>""", unsafe_allow_html=True)

st.write(
    """The France Adventure Planner project is based on the collection and 
    analysis of weather data to help Parisians choose the best weekend 
    destination based on real-time weather conditions. """
)

st.markdown("<a name='Presentation'></a>", unsafe_allow_html=True)

st.markdown("#### Explanation of the Data for This Analysis")
st.write("""
To evaluate the reliability of weather forecasts across France, I collected 
meteorological data for 50 cities from a larger dataset of 250 locations. The data 
was recorded over a two-month period from December 5, 2024, to February 7, 2025, 
and is structured into five separate files, each representing a different 
forecast horizon:

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
- **OpenWeatherMap API **: Provides detailed weather forecasts, including temperature, weather conditions, and rain probability.
- **Nominatim API**: Retrieves latitude and longitude coordinates for selected cities.
- **Scrapy (Web Scraping)**: Extracts hotel recommendations from Booking.com.
- **GitHub Actions**: Automates the script execution to update data daily.
""")

st.markdown("#### - Data collection flow")
# Affiche l'image
st.image("Assets/DataFlow.png", use_container_width=False, width=600)





st.markdown("#### From 250 to 50")
st.write("""Mapping the most Weather-Consistent destinations in France 🌍""")

# Agréger les données en faisant la somme des scores météo par jour
agg_data = all_data.groupby(["Date", "Latitude", "Longitude"], as_index=False)["Weather_Score_jour1"].sum()

fig = px.density_mapbox(
    agg_data,
    lat="Latitude",
    lon="Longitude",
    z="Weather_Score_jour1",  # Influence des données
    mapbox_style="open-street-map",
    animation_frame="Date",  # Animation basée sur la date
    zoom=3.5,
    radius=7,
    color_continuous_scale="thermal",
    center={"lat": 46.603354, "lon": 1.888334},
    labels={"Weather_Score_jour1": "Weather Score"},
    range_color=[agg_data["Weather_Score_jour1"].min(), agg_data["Weather_Score_jour1"].max()]
)

# Affichage
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Why These 50 Cities?")
# Exemple de 50 villes
villes = all_data["Ville"].unique()

# Définir le nombre de colonnes souhaité (ex. 4 colonnes pour un affichage optimisé)
num_cols = 5

# Ajouter des villes vides si nécessaire pour compléter la dernière ligne
while len(villes) % num_cols != 0:
    villes = np.append(villes, "")

# Réorganiser les villes en un DataFrame avec `num_cols` colonnes
df_villes = pd.DataFrame(villes.reshape(-1, num_cols))

# Afficher dans Streamlit
st.dataframe(df_villes, use_container_width=True)

st.markdown("""
    Initially, this project started with a small dataset of 35 cities. 
    However, in order to conduct a more comprehensive and meaningful analysis, 
    I expanded the dataset to include a larger sample of locations. 
    The goal was to capture weather trends across different regions of France rather 
    than focusing solely on individual cities.
    To achieve this, I leveraged ChatGPT to select 50 cities strategically distributed 
    across the French territory. The selection was made based on two key constraints:
    
    - Ensuring a balanced regional distribution to allow for inter-regional comparisons.
    - Including France’s most important cities to make the analysis more relevant and 
    applicable to a larger population.
    
    By expanding the dataset, we gain a broader perspective on the reliability of 
    weather forecasts across France, enabling a more accurate assessment of weather 
    consistency by region.
""")
st.write("---")









st.markdown("<a name='weather-score'></a>", unsafe_allow_html=True)
st.header("🌤️ Weather Score")


st.markdown("## 🏆 <u>Ranking Cities Based on Weather Score</u>", unsafe_allow_html=True)
st.markdown("#### How is the Weather Score Calculated?")
st.markdown("""
    The Weather Score is based on a predefined scoring system, assigning positive or 
    negative values to various weather conditions.
    
    - **Positive scores** are given to pleasant conditions such as clear skies or partial 
    cloud coverage, significantly boosting a city's overall score. 
    - **Negative scores** penalize undesirable conditions like heavy rain, thunderstorms, 
    snow, fog, and severe weather events, reducing the city's total score. 
    
    While this scoring system is somewhat arbitrary, it effectively evaluates 
    and compares weather conditions across different cities.
""")

st.write("#### Top 10 Cities with the Best Weather Scores")

# Calculer le score total pour chaque ville pour le jour 1
city_ranking = all_data.groupby("Ville")["Weather_Score_jour1"].sum().reset_index()
    
# Trier les villes par meilleur score
city_ranking = city_ranking.sort_values(by="Weather_Score_jour1", ascending=False)

# Création de colonnes
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

# Trouver la ville avec le meilleur score
first_city = city_ranking.iloc[0]
second_city = city_ranking.iloc[1]
third_city = city_ranking.iloc[2]

# Colonne de gauche
with col1:
    st.write("**Cities with the Best Weather Scores**")
    st.write(f"🥇 {first_city['Ville']}")
    st.write(f"🥈 {second_city['Ville']}")
    st.write(f"🥉 {third_city['Ville']}")

# Colonne de droite
with col2:    
    st.write("**Total Weather Score**")
    st.write(f"{first_city['Weather_Score_jour1']}")
    st.write(f"{second_city['Weather_Score_jour1']}")
    st.write(f"{third_city['Weather_Score_jour1']}")



# Visualisation du classement en barplot
fig2 = plt.figure(figsize=(12, 8))
sns.barplot(
x="Weather_Score_jour1", 
y="Ville", 
data=city_ranking.head(10), 
palette="plasma"
)

# ajouter les labels sur les barres
for i in range(10):
    plt.text(
        x=city_ranking["Weather_Score_jour1"].iloc[i] + 0.1,
        y=i,
        s=city_ranking["Weather_Score_jour1"].iloc[i],
        ha="right",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="white"
    )

# Modifier la couleur des labels et du titre
plt.xlabel("Weather Score (Sum)", fontsize=12, color="black")
plt.ylabel("City", fontsize=12, color="black")

# Modifier la couleur des axes
plt.xticks(color="black")
plt.yticks(color="black")

# Affichage du graphique dans Streamlit
st.pyplot(fig2)

st.markdown("""
    The bar chart above clearly illustrates the ranking of the top 10 French cities 
    based on their weather scores. The results highlight significant regional patterns, 
    showcasing southern France as the region with the most favorable weather conditions. 
    The cities at the top of this ranking enjoy consistently higher weather scores, 
    reflecting an appealing climate that attracts both residents and visitors seeking 
    optimal weather throughout the year.
""")
st.write("")
st.write("")

st.write("#### Top 10 Cities with the Lowest Weather Scores")
# Trier les villes par pire score
city_ranking_end = city_ranking.sort_values(by="Weather_Score_jour1", ascending=True)

# Création de colonnes
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

# Trouver la ville avec le meilleur score
worst_city = city_ranking_end.iloc[0]
second_worst_city = city_ranking_end.iloc[1]
third_worst_city = city_ranking_end.iloc[2]


# Colonne de gauche
with col1:
    st.write("**Cities with the Lowest Weather Scores**")
    st.write(f"{worst_city['Ville']}")
    st.write(f"{second_worst_city['Ville']}")
    st.write(f"{third_worst_city['Ville']}")

# Colonne de droite
with col2:    
    st.write("**Total Weather Score**")
    st.write(f"{worst_city['Weather_Score_jour1']}")
    st.write(f"{second_worst_city['Weather_Score_jour1']}")
    st.write(f"{third_worst_city['Weather_Score_jour1']}")


# Visualisation du classement en barplot
fig2 = plt.figure(figsize=(12, 8))
sns.barplot(
x="Weather_Score_jour1", 
y="Ville", 
data=city_ranking_end.head(10), 
palette="viridis"
)

# ajouter les labels sur les barres
for i in range(10):
    plt.text(
        x=city_ranking_end["Weather_Score_jour1"].iloc[i] + 0.1,
        y=i,
        s=city_ranking_end["Weather_Score_jour1"].iloc[i],
        ha="right",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="white"
    )

# Modifier la couleur des labels et du titre
plt.xlabel("Weather Score (Sum)", fontsize=12, color="black")
plt.ylabel("City", fontsize=12, color="black")

# Modifier la couleur des axes
plt.xticks(color="black")
plt.yticks(color="black")

# Affichage du graphique dans Streamlit
st.pyplot(fig2)

st.markdown("""
    This bar chart presents the 10 cities in France with the lowest overall weather 
    scores. The results notably reveal that cities primarily located in northern and 
    northwestern regions have the least favorable weather conditions. These cities 
    typically experience lower scores due to factors such as frequent rainfall, cooler 
    temperatures, and less sunshine, making them comparatively less attractive in terms 
    of weather comfort.
""")

st.write("#### Top 25 and Bottom 25 Cities on the French Map")
# Weather_Score map
if all(col in all_data.columns for col in ["Weather_Score_jour1", "Latitude", "Longitude"]):
    
    # Calculer le score total pour chaque ville pour le jour 1
    city_ranking = all_data.groupby("Ville", as_index=False).agg({
        "Weather_Score_jour1": "sum",
        "Latitude": "first",
        "Longitude": "first"
    })
    
    # Trier les villes par meilleur score
    city_ranking = city_ranking.sort_values(by="Weather_Score_jour1", ascending=False)

    # Sélectionner les 25 meilleures et les 25 pires villes
    top_25_cities = city_ranking.head(25).copy()
    worst_25_cities = city_ranking.tail(25).copy()

    # Ajouter une colonne pour différencier les catégories
    top_25_cities["Category"] = "Top 25"
    worst_25_cities["Category"] = "Worst 25"

    # Fusionner les deux catégories
    top_worst_cities = pd.concat([top_25_cities, worst_25_cities])

    # Appliquer une taille uniforme pour toutes les villes
    top_worst_cities["Size"] = 5  # Taille fixe pour tous les points

    # Définir une palette de couleurs : Rouge pour le Top 25, Bleu pour le Worst 25
    color_map = {"Top 25": "red", "Worst 25": "blue"}

    # Carte interactive des 25 meilleures et 25 pires villes
    fig3 = px.scatter_mapbox(
        top_worst_cities,
        lat="Latitude",
        lon="Longitude",
        color="Category",  
        size="Size",  
        hover_name="Ville",
        hover_data={"Weather_Score_jour1": True},
        mapbox_style="open-street-map",
        zoom=3.5,
        color_discrete_map=color_map,
        size_max=10  
    )

    st.plotly_chart(fig3, use_container_width=True)

else:
    st.write("Some columns are missing. Please check the dataset.")

st.markdown("""
    This interactive map highlights the geographical distribution of the best (red) 
    and worst (blue) performing cities based on their overall Weather Scores. A clear 
    pattern emerges, with the top-ranking cities primarily located in southern France, 
    benefiting from more favorable climatic conditions. Conversely, the lowest-ranking 
    cities cluster predominantly in northern and northwestern regions, indicating less 
    favorable weather patterns.
    This visualization offers an intuitive geographical perspective on regional weather 
    differences across France.
""")

st.write("---")










st.markdown("<a name='temperature'></a>", unsafe_allow_html=True)
st.header("🌡️ Temperature")

# Afficher la temperature moyenne par jour pour chaque ville
st.write("#### Evolution of the average Temperature per Day")
Temp_date = (all_data.groupby("Date")["Temp_Avg_jour1"].mean())

# Affichage sur un lineplot
fig10 = plt.figure(figsize=(18, 8))
sns.lineplot(
    x=Temp_date.index,
    y=Temp_date.values,
    marker="o",
    color="blue",
    linewidth=2,
    markersize=8
)

# Modifier la couleur des labels et du titre
plt.xlabel("Date", fontsize=12, color="black", fontweight="bold")
plt.ylabel("Average Temperature", fontsize=12, color="black", fontweight="bold")
plt.xticks(rotation=90, fontsize=10, color="black")
plt.yticks(fontsize=10, color="black")

# Modifier la couleur des axes
plt.xticks(color="black")
plt.yticks(color="black")

# Affichage du graphique dans Streamlit
st.pyplot(fig10)

st.markdown("""
    This line chart shows the daily average temperature over the analyzed period. 
    A notable drop in temperatures is clearly visible, corresponding to the recent 
    cold wave experienced across France. This significant temperature decline underscores 
    the severity of this weather event, providing valuable context for understanding 
    temperature fluctuations during the winter season.
""")


st.markdown("## 🏆 <u>Ranking Cities Based on Temperature</u>", unsafe_allow_html=True)

st.write("#### Top 10 Cities with the Highest Temperature")

# Calculer la avg_temp pour chaque ville pour le jour 1
city_temp = all_data.groupby("Ville")["Temp_Avg_jour1"].mean().reset_index()
    
# Trier les villes par température
city_temp = city_temp.sort_values(by="Temp_Avg_jour1", ascending=False)

# Création de colonnes
col5, col6 = st.columns(2, gap="small", vertical_alignment="center")

# Trouver la ville avec la meilleur température
first_city_temp = city_temp.iloc[0]
second_city_temp = city_temp.iloc[1]
third_city_temp = city_temp.iloc[2]

# Colonne de gauche
with col5:
    st.write("**Cities with the Best Average temperature**")
    st.write(f"🥇 {first_city_temp['Ville']}")
    st.write(f"🥈 {second_city_temp['Ville']}")
    st.write(f"🥉 {third_city_temp['Ville']}")

# Colonne de droite
with col6:    
    st.write("**Overall Average Temperature**")
    st.write(f"{first_city_temp['Temp_Avg_jour1']:.2f}")
    st.write(f"{second_city_temp['Temp_Avg_jour1']:.2f}")
    st.write(f"{third_city_temp['Temp_Avg_jour1']:.2f}")



# Visualisation du classement en barplot
fig4 = plt.figure(figsize=(12, 8))
sns.barplot(
x="Temp_Avg_jour1", 
y="Ville", 
data=city_temp.head(10), 
palette="plasma"
)

# ajouter les labels sur les barres
for i in range(10):
    plt.text(
        x=city_temp["Temp_Avg_jour1"].iloc[i] + 0.1,
        y=i,
        s=f"{city_temp['Temp_Avg_jour1'].iloc[i]:.2f}",
        ha="left",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="black"
    )

# Modifier la couleur des labels et du titre
plt.xlabel("Average Temperature", fontsize=12, color="black")
plt.ylabel("City", fontsize=12, color="black")

# Modifier la couleur des axes
plt.xticks(color="black")
plt.yticks(color="black")

# Affichage du graphique dans Streamlit
st.pyplot(fig4)

st.markdown("""
    This visualization highlights the top 10 French cities with the highest average 
    temperatures. The results clearly emphasize the milder and warmer climates in the 
    southern regions of France. These cities are characterized by higher average 
    temperatures, making them particularly appealing destinations for visitors and 
    residents who appreciate a warmer climate throughout the year.
""")
st.write("")
st.write("")

st.write("#### Top 10 Cities with the Lowest Temperature")
# Trier les villes par pire score
city_temp_end = city_temp.sort_values(by="Temp_Avg_jour1", ascending=True)

# Création de colonnes
col7, col8 = st.columns(2, gap="small", vertical_alignment="center")

# Trouver la ville avec le meilleur score
worst_city_temp = city_temp_end.iloc[0]
second_worst_city_temp = city_temp_end.iloc[1]
third_worst_city_temp = city_temp_end.iloc[2]


# Colonne de gauche
with col7:
    st.write("**Cities with the Lowest Temperature**")
    st.write(f"{worst_city_temp['Ville']}")
    st.write(f"{second_worst_city_temp['Ville']}")
    st.write(f"{third_worst_city_temp['Ville']}")

# Colonne de droite
with col8:    
    st.write("**Overall Average Temperature**")
    st.write(f"{worst_city_temp['Temp_Avg_jour1']:.2f}")
    st.write(f"{second_worst_city_temp['Temp_Avg_jour1']:.2f}")
    st.write(f"{third_worst_city_temp['Temp_Avg_jour1']:.2f}")


# Visualisation du classement en barplot
fig5 = plt.figure(figsize=(12, 8))
sns.barplot(
x="Temp_Avg_jour1", 
y="Ville", 
data=city_temp_end.head(10), 
palette="viridis"
)

# ajouter les labels sur les barres
for i in range(10):
    plt.text(
        x=city_temp_end["Temp_Avg_jour1"].iloc[i] + 0.1,
        y=i,
        s=f"{city_temp_end['Temp_Avg_jour1'].iloc[i]:.2f}",
        ha="left",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="black"
    )

# Modifier la couleur des labels et du titre
plt.xlabel("Weather Score (Sum)", fontsize=12, color="black")
plt.ylabel("City", fontsize=12, color="black")

# Modifier la couleur des axes
plt.xticks(color="black")
plt.yticks(color="black")

# Affichage du graphique dans Streamlit
st.pyplot(fig5)

st.markdown("""
    This bar chart highlights the French cities with the lowest average temperatures. 
    The results show a clear tendency for colder climates primarily in mountainous and 
    eastern regions. These cities experience notably lower temperatures, with some even 
    averaging below freezing, making them ideal locations for winter sports and related 
    outdoor activities, but less appealing for those seeking warmer conditions.
""")



st.write("#### Top 25 and Bottom 25 Cities on the French Map")
# Weather_Score map
if all(col in all_data.columns for col in ["Temp_Avg_jour1", "Latitude", "Longitude"]):
    
    # Calculer le score total pour chaque ville pour le jour 1
    city_temp = all_data.groupby("Ville", as_index=False).agg({
        "Temp_Avg_jour1": "mean",
        "Latitude": "first",
        "Longitude": "first"
    })
    
    # Trier les villes par meilleur score
    city_temp = city_temp.sort_values(by="Temp_Avg_jour1", ascending=False)

    # Sélectionner les 25 meilleures et les 25 pires villes
    top_25_cities = city_temp.head(25).copy()
    worst_25_cities = city_temp.tail(25).copy()

    # Ajouter une colonne pour différencier les catégories
    top_25_cities["Category"] = "Top 25"
    worst_25_cities["Category"] = "Worst 25"

    # Fusionner les deux catégories
    top_worst_cities = pd.concat([top_25_cities, worst_25_cities])

    # Appliquer une taille uniforme pour toutes les villes
    top_worst_cities["Size"] = 5  # Taille fixe pour tous les points

    # Définir une palette de couleurs : Rouge pour le Top 5, Bleu pour le Worst 5
    color_map = {"Top 25": "red", "Worst 25": "blue"}

    # Carte interactive des 25 meilleures et 25 pires villes
    fig6 = px.scatter_mapbox(
        top_worst_cities,
        lat="Latitude",
        lon="Longitude",
        color="Category",  
        size="Size",  
        hover_name="Ville",
        hover_data={"Temp_Avg_jour1": True},
        mapbox_style="open-street-map",
        zoom=3.5,
        color_discrete_map=color_map,
        size_max=10  
    )

    st.plotly_chart(fig6, use_container_width=True)

else:
    st.write("Some columns are missing. Please check the dataset.")

st.markdown("""
    This interactive map visually summarizes the geographic distribution of the cities 
    with the highest (red) and lowest (blue) average temperatures across France. 
    A distinct pattern emerges: warmer cities are predominantly located in the south 
    and coastal areas, benefiting from milder climates. In contrast, cities with colder 
    average temperatures are mostly situated in eastern and mountainous regions, 
    characterized by harsher, cooler climates.
    This map effectively illustrates the clear climatic variations and regional 
    differences in temperature across the country.
""")
st.write("---")










st.markdown("<a name='rain-probability'></a>", unsafe_allow_html=True)
st.header("🌧️ Rain Probability")


st.markdown("## 🏆 <u>Ranking Cities Based on Rain Probability</u>", unsafe_allow_html=True)

# Calculer la avg_temp pour chaque ville pour le jour 1
city_rain = all_data.groupby("Ville")["Rain_Probability_jour1"].sum().reset_index()
    
# Trier les villes
city_rain = city_rain.sort_values(by="Rain_Probability_jour1", ascending=False)


st.write("#### Top 10 Cities with the Lowest Probability of Rain")
# Trier les villes par pire score
city_rain_end = city_rain.sort_values(by="Rain_Probability_jour1", ascending=True)

# Création de colonnes
col11, col12 = st.columns(2, gap="small", vertical_alignment="center")

# Trouver la ville avec le meilleur score
worst_city_rain = city_rain_end.iloc[0]
second_worst_city_rain = city_rain_end.iloc[1]
third_worst_city_rain = city_rain_end.iloc[2]


# Colonne de gauche
with col11:
    st.write("**Cities with the Lowest Rain Probability**")
    st.write(f"🥇 {worst_city_rain['Ville']}")
    st.write(f"🥈 {second_worst_city_rain['Ville']}")
    st.write(f"🥉 {third_worst_city_rain['Ville']}")

# Colonne de droite
with col12:    
    st.write("**Total Rain Probability**")
    st.write(f"{worst_city_rain['Rain_Probability_jour1']:.2f}")
    st.write(f"{second_worst_city_rain['Rain_Probability_jour1']:.2f}")
    st.write(f"{third_worst_city_rain['Rain_Probability_jour1']:.2f}")


# Visualisation du classement en barplot
fig8 = plt.figure(figsize=(12, 8))
sns.barplot(
x="Rain_Probability_jour1", 
y="Ville", 
data=city_rain_end.head(10), 
palette="plasma"
)

# ajouter les labels sur les barres
for i in range(10):
    plt.text(
        x=city_rain_end["Rain_Probability_jour1"].iloc[i] + 0.1,
        y=i,
        s=f"{city_rain_end['Rain_Probability_jour1'].iloc[i]:.2f}",
        ha="right",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="white"
    )

# Modifier la couleur des labels et du titre
plt.xlabel("Rain Probability (Sum)", fontsize=12, color="black")
plt.ylabel("City", fontsize=12, color="black")

# Modifier la couleur des axes
plt.xticks(color="black")
plt.yticks(color="black")

# Affichage du graphique dans Streamlit
st.pyplot(fig8)

st.markdown("""
    This visualization highlights the French cities least likely to experience rainfall, 
    making them particularly appealing destinations for travelers seeking dry and sunny 
    weather. The cities topping this ranking have notably low cumulative rain 
    probabilities, indicating consistently drier conditions compared to other regions. 
    Such insights are valuable for planning activities sensitive to weather conditions, 
    ensuring visitors and residents can fully enjoy their outdoor experiences.
""")
st.write("")
st.write("")



st.write("#### Top 10 Cities with the Highest Probability of Rain")
# Création de colonnes
col9, col10 = st.columns(2, gap="small", vertical_alignment="center")

# Trouver la ville avec la meilleur Rain Probability
first_city_rain = city_rain.iloc[0]
second_city_rain = city_rain.iloc[1]
third_city_rain = city_rain.iloc[2]

# Colonne de gauche
with col9:
    st.write("**Cities with the Highest Probability of rain**")
    st.write(f"{first_city_rain['Ville']}")
    st.write(f"{second_city_rain['Ville']}")
    st.write(f"{third_city_rain['Ville']}")

# Colonne de droite
with col10:    
    st.write("**Total Rain Probability**")
    st.write(f"{first_city_rain['Rain_Probability_jour1']:.2f}")
    st.write(f"{second_city_rain['Rain_Probability_jour1']:.2f}")
    st.write(f"{third_city_rain['Rain_Probability_jour1']:.2f}")



# Visualisation du classement en barplot
fig7 = plt.figure(figsize=(12, 8))
sns.barplot(
x="Rain_Probability_jour1", 
y="Ville", 
data=city_rain.head(10), 
palette="viridis"
)

# ajouter les labels sur les barres
for i in range(10):
    plt.text(
        x=city_rain["Rain_Probability_jour1"].iloc[i] + 0.1,
        y=i,
        s=f"{city_rain['Rain_Probability_jour1'].iloc[i]:.2f}",
        ha="right",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="white"
    )

# Modifier la couleur des labels et du titre
plt.xlabel("Rain Probability (sum)", fontsize=12, color="black")
plt.ylabel("City", fontsize=12, color="black")

# Modifier la couleur des axes
plt.xticks(color="black")
plt.yticks(color="black")

# Affichage du graphique dans Streamlit
st.pyplot(fig7)

st.markdown("""
    This chart identifies the French cities most likely to experience rainfall. 
    The cities at the top of this ranking have notably high cumulative probabilities, 
    highlighting regions more prone to rainy weather. These insights are particularly 
    valuable for planning outdoor activities or travels, as visitors and residents might 
    prefer to be prepared for wetter conditions or consider alternative destinations.
""")


st.write("#### Top 25 and Bottom 25 Cities on the Map")
# Rain_Probability map
if all(col in all_data.columns for col in ["Rain_Probability_jour1", "Latitude", "Longitude"]):
    
    # Calculer le score total pour chaque ville pour le jour 1
    city_rain = all_data.groupby("Ville", as_index=False).agg({
        "Rain_Probability_jour1": "sum",
        "Latitude": "first",
        "Longitude": "first"
    })
    
    # Trier les villes par meilleur score
    city_rain = city_rain.sort_values(by="Rain_Probability_jour1", ascending=False)

    # Sélectionner les 25 meilleures et les 25 pires villes
    top_25_cities_rain = city_rain.head(25).copy()
    worst_25_cities_rain = city_rain.tail(25).copy()

    # Ajouter une colonne pour différencier les catégories
    top_25_cities_rain["Category"] = "High Prob 25"
    worst_25_cities_rain["Category"] = "Low Prob 25"

    # Fusionner les deux catégories
    top_worst_cities_rain = pd.concat([top_25_cities_rain, worst_25_cities_rain])

    # Appliquer une taille uniforme pour toutes les villes
    top_worst_cities_rain["Size"] = 5  # Taille fixe pour tous les points

    # Définir une palette de couleurs : Rouge pour le Top 5, Bleu pour le Worst 5
    color_map = {"Low Prob 25": "red", "High Prob 25": "blue"}

    # Carte interactive des 25 meilleures et 25 pires villes
    fig9 = px.scatter_mapbox(
        top_worst_cities_rain,
        lat="Latitude",
        lon="Longitude",
        color="Category",  
        size="Size",  
        hover_name="Ville",
        hover_data={"Rain_Probability_jour1": True},
        mapbox_style="open-street-map",
        zoom=3.5,
        color_discrete_map=color_map,
        size_max=10  
    )

    st.plotly_chart(fig9, use_container_width=True)

else:
    st.write("Some columns are missing. Please check the dataset.")

st.markdown("""
    This map provides an insightful visualization of rainfall probability across French 
    cities, clearly highlighting distinct regional patterns:
            
    - Southern France, especially the Mediterranean coast, emerges as notably drier, 
    with the lowest probabilities of rainfall. This is due to the influence of the 
    Mediterranean climate, characterized by mild, wet winters but predominantly sunny 
    and dry weather throughout most of the year.
    - Conversely, the northern and northwestern coastal regions, particularly along 
    the Atlantic coast, experience significantly higher rainfall. Cities in these areas 
    are more exposed to prevailing oceanic weather patterns, leading to frequent 
    precipitation and humid conditions.
    - Additionally, cities in mountainous and eastern regions reflect higher rainfall 
    probabilities due to the influence of local topography, which promotes more frequent 
    precipitation and cooler climates.
            
    This geographical insight allows travelers, residents, and businesses to better 
    anticipate and prepare for regional weather conditions in France.
""")
st.write("---")










st.markdown("<a name='accuracy'></a>", unsafe_allow_html=True)

# Liste des jours à comparer avec la référence (jour 1)
jours_previsions = ["jour2", "jour3", "jour4", "jour5"]

# Calcul des écarts relatifs pour chaque jour de prévision par rapport à jour1
for jour in jours_previsions:
    all_data[f"Temp_Error_{jour}"] = abs(all_data[f"Temp_Avg_{jour}"] - all_data["Temp_Avg_jour1"]) / all_data["Temp_Avg_jour1"]
    all_data[f"Rain_Error_{jour}"] = abs(all_data[f"Rain_Probability_{jour}"] - all_data["Rain_Probability_jour1"])
    all_data[f"Weather_Score_Error_{jour}"] = abs(all_data[f"Weather_Score_{jour}"] - all_data["Weather_Score_jour1"]) / 200

# Score d'accuracy basé sur les écarts
for jour in jours_previsions:
    all_data[f"Accuracy_{jour}"] = 100 - (
        (all_data[f"Temp_Error_{jour}"] * 40) + 
        (all_data[f"Rain_Error_{jour}"] * 35) + 
        (all_data[f"Weather_Score_Error_{jour}"] * 25)
    )

# Normalisation du score pour qu'il reste entre 0 et 100
for jour in jours_previsions:
    all_data[f"Accuracy_{jour}"] = all_data[f"Accuracy_{jour}"].clip(0, 100)

# Affichage des résultats
all_data[["Ville", "Date"] + [f"Accuracy_{jour}" for jour in jours_previsions]].head()

# regrouper pour chaque ville
city_accuracy = all_data.groupby("Ville")[[f"Accuracy_{jour}" for jour in jours_previsions]].mean()
# Calculer la moyenne des scores d'accuracy pour chaque ville et garder les latitudes et longitudes
city_accuracy = all_data.groupby("Ville")[[f"Accuracy_{jour}" for jour in jours_previsions]].mean().reset_index()
# Calculer la moyenne des scores d'accuracy pour chaque ville
city_accuracy["Mean_Accuracy"] = city_accuracy[[f"Accuracy_{jour}" for jour in jours_previsions]].mean(axis=1)
# Trier les villes par la moyenne des scores d'accuracy
city_accuracy = city_accuracy.sort_values(by="Mean_Accuracy", ascending=False)
# incorporer le score d'accuracy dans le DataFrame
city_accuracy_lat_long = pd.merge(city_accuracy, all_data[["Ville", "Latitude", "Longitude"]], on="Ville")
# Drop duplicates
city_accuracy_lat_long = city_accuracy.drop_duplicates(subset=["Ville"])

st.header("🎯 Accuracy of Weather Predictions")

st.markdown("""
    Weather forecasts play a crucial role in planning daily activities, 
    travel, and outdoor events. However, their reliability varies based on 
    multiple factors, such as region, season, and forecast timeframe.
    This application analyzes the accuracy of weather forecasts by comparing 
    predicted weather conditions with actual recorded data. It calculates 
    key error metrics, including absolute and relative errors, to assess 
    the precision of different forecast models over time.
    With interactive visualizations and statistical insights, Weather 
    Accuracy provides users with a clear understanding of forecast 
    performance, helping them make more informed decisions based on 
    real-world data.
""")

st.markdown("""
    ### How is the Accuracy Score Calculated?  

    The accuracy score in this application measures the reliability of weather forecasts 
    by comparing predicted values with actual recorded data. It is based on three key weather parameters:  

    - **Temperature Accuracy**: The relative error between the forecasted and actual average temperature.  
    - **Rain Probability Accuracy**: The absolute difference between the predicted and actual probability of rain.  
    - **Weather Score Accuracy**: A normalized error based on the general weather condition score (ranging from 0 to 200).  

    #### Error Calculation for Each Forecast Day  

    The errors are computed as follows:  

    - **Temperature Error** = |Forecasted Temperature - Actual Temperature| / Actual Temperature  
    - **Rain Probability Error** = |Forecasted Rain Probability - Actual Rain Probability|  
    - **Weather Score Error** = |Forecasted Weather Score - Actual Weather Score| / 200  

    #### Weighting the Errors  

    Each error contributes to the final accuracy score with a specific weight:  

    - **40% weight on Temperature Error** (temperature is a key factor in weather perception)  
    - **35% weight on Rain Probability Error** (rain directly impacts daily plans)  
    - **25% weight on Weather Score Error** (a general indicator of weather conditions)  

    The **accuracy score** for each forecast day is calculated as:  

    ```
    Accuracy = 100 - ((Temp_Error * 40) + (Rain_Error * 30) + (Weather_Score_Error * 30))
    ```

    This ensures that **a lower error leads to a higher accuracy score**, with values normalized between **0 and 100** 
    (where 100 represents a perfect forecast match).  

    #### City-Level Accuracy  

    To assess the overall forecast performance per city, the accuracy scores for all forecast days are averaged, 
    resulting in a **Mean Accuracy Score** for each city.  

    This approach allows users to identify **which locations have the most reliable weather predictions** 
    and adjust their plans accordingly.  
""")

st.markdown("""
    ## How Reliable Are Weather Forecasts?  
    Forecast accuracy decreases over time: while predictions for **Day +1** 
    remain highly reliable, confidence gradually declines by **Day +4**, 
    where forecasts should be considered with more caution.
""")


col60, col61, col62, col63 = st.columns(4)
col60.metric("**Accuracy Day +1**", f"{city_accuracy['Accuracy_jour2'].mean():.2f}%")
col61.metric("**Accuracy Day +2**", f"{city_accuracy['Accuracy_jour3'].mean():.2f}%")
col62.metric("**Accuracy Day +3**", f"{city_accuracy['Accuracy_jour4'].mean():.2f}%")
col63.metric("**Accuracy Day +4**", f"{city_accuracy['Accuracy_jour5'].mean():.2f}%")

col64, col65 = st.columns(2, gap="small", vertical_alignment="center")
col64.image("Assets/Flag.png", use_container_width=False, width=500)
France_accuracy = city_accuracy["Mean_Accuracy"].mean()
with col65:
    st.markdown(f"""
    ### National Accuracy Score
    The average weather forecast accuracy across the entire French territory 
    is {France_accuracy:.2f} This score reflects the overall reliability of weather predictions based 
    on historical comparisons.
    """)

    st.metric("**Accuracy Score**",f"{France_accuracy:.2f}%")
# sauter 3 lignes
st.write("")
st.write("")
st.write("")

st.write("#### Top 10 Cities with the Highest Accuracy")

# Création de colonnes
col13, col14 = st.columns(2, gap="small", vertical_alignment="center")

# Trouver la ville avec le meilleur score
best_city_accuracy = city_accuracy.iloc[0]
second_best_city_accuracy = city_accuracy.iloc[1]
third_best_city_accuracy = city_accuracy.iloc[2]


# Colonne de gauche
with col13:
    st.write("**Cities with the Highest Accuracy**")
    st.write(f"🥇 {best_city_accuracy['Ville']}")
    st.write(f"🥈 {second_best_city_accuracy['Ville']}")
    st.write(f"🥉 {third_best_city_accuracy['Ville']}")

# Colonne de droite
with col14:    
    st.write("**Probability**")
    st.write(f"{best_city_accuracy['Mean_Accuracy']:.2f}%")
    st.write(f"{second_best_city_accuracy['Mean_Accuracy']:.2f}%")
    st.write(f"{third_best_city_accuracy['Mean_Accuracy']:.2f}%")


# Visualisation du classement en barplot
fig11 = plt.figure(figsize=(12, 8))
sns.barplot(
    x="Mean_Accuracy",
    y="Ville",
    data=city_accuracy.head(10),
    palette="plasma"
)

# ajouter les labels sur les barres
for i in range(10):
    plt.text(
        x=city_accuracy["Mean_Accuracy"].iloc[i] + 0.1,
        y=i,
        s=f"{city_accuracy['Mean_Accuracy'].iloc[i]:.2f}%",
        ha="right",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="white"
    )

# Modifier la couleur des labels et du titre
plt.xlabel("Mean Accuracy Score", fontsize=12, color="black")
plt.ylabel("City", fontsize=12, color="black")

# Modifier la couleur des axes
plt.xticks(color="black")
plt.yticks(color="black")  

# Affichage du graphique dans Streamlit
st.pyplot(fig11)

st.markdown("""
    This chart showcases the cities in France where weather forecasts are 
    the most reliable. The rankings suggest that certain regions, particularly 
    coastal and mountainous areas, benefit from more precise weather predictions.
    The high accuracy in these cities may be influenced by stable meteorological 
    conditions, well-monitored climate patterns, or advanced forecasting models 
    used for these locations.
            
    This data can help individuals and businesses better assess how much they 
    can trust weather forecasts when planning activities, particularly in regions
    with high forecast reliability.
""")

st.write("")

st.write("#### Top 10 Cities with the Lowest Accuracy")

# Création de colonnes
col15, col16 = st.columns(2, gap="small", vertical_alignment="center")

# Trouver la ville avec le meilleur score
worst_city_accuracy = city_accuracy.iloc[-1]
second_worst_city_accuracy = city_accuracy.iloc[-2]
third_worst_city_accuracy = city_accuracy.iloc[-3]


# Colonne de gauche
with col15:
    st.write("**Cities with the Highest Accuracy Score**")
    st.write(f"{worst_city_accuracy['Ville']}")
    st.write(f"{second_worst_city_accuracy['Ville']}")
    st.write(f"{third_worst_city_accuracy['Ville']}")

# Colonne de droite
with col16:    
    st.write("**Probability**")
    st.write(f"{worst_city_accuracy['Mean_Accuracy']:.2f}%")
    st.write(f"{second_worst_city_accuracy['Mean_Accuracy']:.2f}%")
    st.write(f"{third_worst_city_accuracy['Mean_Accuracy']:.2f}%")


end_accuracy = city_accuracy.sort_values(by="Mean_Accuracy", ascending=True)
# Visualisation du classement en barplot
fig12 = plt.figure(figsize=(12, 8))
sns.barplot(
    x="Mean_Accuracy",
    y="Ville",
    data=end_accuracy.head(10),
    palette="viridis"
)

# ajouter les labels sur les barres
for i in range(10):
    plt.text(
        x=end_accuracy["Mean_Accuracy"].iloc[i] + 0.1,
        y=i,
        s=f"{end_accuracy['Mean_Accuracy'].iloc[i]:.2f}%",
        ha="right",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="white"
    )

# Modifier la couleur des labels et du titre
plt.xlabel("Mean Accuracy Score", fontsize=12, color="black")
plt.ylabel("City", fontsize=12, color="black")

# Modifier la couleur des axes
plt.xticks(color="black")
plt.yticks(color="black")  

# Affichage du graphique dans Streamlit
st.pyplot(fig12)

st.markdown("""
    This chart highlights the cities where weather forecasts have shown the 
    lowest accuracy rates. The results suggest that forecasts in these locations 
    tend to be less reliable, which could be due to more unpredictable weather 
    patterns, local climate variability, or geographical influences.
            
    While forecasts in these cities still maintain a reasonable accuracy level, 
    greater uncertainty should be expected, especially for long-term predictions.
    This information is useful for individuals and businesses that rely on 
    precise weather forecasts for planning purposes.
""")
st.write("")

# Fusionner les données de latitude et longitude avec city_accuracy
city_accuracy_lat_long = city_accuracy.merge(
    all_data[["Ville", "Latitude", "Longitude"]].drop_duplicates(),
    on="Ville",
    how="left"
)

st.write("#### Geographical Distribution of Forecast Accuracy")
# Sélectionner les 25 meilleures et les 25 pires villes
top_25_cities_accurate = city_accuracy_lat_long.head(25).copy()
worst_25_cities_accurate = city_accuracy_lat_long.tail(25).copy()
# Ajouter une colonne pour différencier les catégories
top_25_cities_accurate["Category"] = "High Prob 25"
worst_25_cities_accurate["Category"] = "Low Prob 25"   
# Fusionner les deux catégories
top_worst_cities_accurate = pd.concat([top_25_cities_accurate, worst_25_cities_accurate])
# Appliquer une taille uniforme pour toutes les villes
top_worst_cities_accurate["Size"] = 5  # Taille fixe pour tous les points

# Définir une palette de couleurs : Rouge pour le Top 5, Bleu pour le Worst 5
color_map = {"High Prob 25": "red", "Low Prob 25": "blue"}

# Carte interactive des 25 meilleures et 25 pires villes
fig15 = px.scatter_mapbox(
        top_worst_cities_accurate,
        lat="Latitude",
        lon="Longitude",
        color="Category",  
        size="Size",  
        hover_name="Ville",
        hover_data={"Mean_Accuracy": True},
        mapbox_style="open-street-map",
        zoom=3.5,
        color_discrete_map=color_map,
        size_max=10  
    )

st.plotly_chart(fig15, use_container_width=True)

st.markdown("""
    This map visualizes the top 25 cities with the highest forecast accuracy 
    (in red) and the 25 cities with the lowest forecast accuracy (in blue).
    Southern and coastal regions, marked in red, tend to have more reliable 
    weather predictions, likely due to more stable climate conditions and 
    better forecasting models for these areas.
            
    Central and northern cities, marked in blue, show lower forecast accuracy, 
    which could be influenced by more unpredictable weather patterns, frequent 
    atmospheric changes, or local geographical factors.
            
    This spatial distribution highlights how forecast accuracy varies across 
    France, helping users better understand which regions have the most and 
    least dependable weather forecasts.
""")

st.markdown("### Are Weather forecasts over-optimistic or pessimistic?")
st.markdown("""
    In this section, I aimed to analyze whether weather forecasts tend to be
    overly optimistic or pessimistic across different meteorological aspects.
    By comparing predicted and actual values for **weather scores**, **temperature**,
    **rain probability**, and **humidity** over multiple days, I sought to identify
    potential forecasting biases. 
            
    Understanding these trends helps assess the reliability of forecasts and 
    whether adjustments should be made when interpreting them over time.
""")

# Extraire les Scores météo pour chaque jour avec les bons suffixes
weather_socre_avg = {
    "Day +1": all_data["Weather_Score_jour1"].mean(),
    "Day +2": all_data["Weather_Score_jour2"].mean(),
    "Day +3": all_data["Weather_Score_jour3"].mean(),
    "Day +4": all_data["Weather_Score_jour4"].mean(),
    "Day +5": all_data["Weather_Score_jour5"].mean(),
}
# Extraire les Temperatures pour chaque jour avec les bons suffixes
Temp_Avg = {
    "Day +1": all_data["Temp_Avg_jour1"].mean(),
    "Day +2": all_data["Temp_Avg_jour2"].mean(),
    "Day +3": all_data["Temp_Avg_jour3"].mean(),
    "Day +4": all_data["Temp_Avg_jour4"].mean(),
    "Day +5": all_data["Temp_Avg_jour5"].mean(),
}
# Extraire les Rain_Probability pour chaque jour avec les bons suffixes
Rain_Prob = {
    "Day +1": all_data["Rain_Probability_jour1"].mean(),
    "Day +2": all_data["Rain_Probability_jour2"].mean(),
    "Day +3": all_data["Rain_Probability_jour3"].mean(),
    "Day +4": all_data["Rain_Probability_jour4"].mean(),
    "Day +5": all_data["Rain_Probability_jour5"].mean(),
}
# Extraire les Rain_Probability pour chaque jour avec les bons suffixes
Humidity_Prob = {
    "Day +1": all_data["Humidity_jour1"].mean(),
    "Day +2": all_data["Humidity_jour2"].mean(),
    "Day +3": all_data["Humidity_jour3"].mean(),
    "Day +4": all_data["Humidity_jour4"].mean(),
    "Day +5": all_data["Humidity_jour5"].mean(),
}

# Fonction pour créer un lineplot amélioré
def create_lineplot(data, title, xlabel, ylabel, color):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(list(data.keys()), list(data.values()), marker="o", linestyle="-", color=color, linewidth=2)
    
    # Ajouter les valeurs sur les points
    for i, txt in enumerate(data.values()):
        ax.annotate(f"{txt:.2f}", (list(data.keys())[i], txt), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=10, fontweight="bold")

    #ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.grid(True)
    return fig

# Création des graphiques
fig_weather = create_lineplot(weather_socre_avg, "Weather Score", "Day", "Weather Score", "purple")
fig_temp = create_lineplot(Temp_Avg, "Temperature", "Day", "Average Temperature", "red")
fig_rain = create_lineplot(Rain_Prob, "Rain Probability", "Day", "Rain Probability", "blue")
fig_humidity = create_lineplot(Humidity_Prob, "Humidity", "Day", "Average Humidity", "green")

# Afficher les graphiques
col17, col18 = st.columns(2)
col17.pyplot(fig_weather)
col18.pyplot(fig_temp)

col19, col22 = st.columns(2)
col19.pyplot(fig_rain)
col22.pyplot(fig_humidity)

# 📌 Ajout d’une section d'interprétation après les graphiques
st.markdown("#### 🔎  Key Insights from the Forecast Bias Analysis")

st.markdown("""
    ✅ Weather Score Trends:
    - The forecasted weather score increases as the forecast horizon extends 
    (Day +5 is higher than Day +1).
    - This suggests that longer-term forecasts tend to be overly optimistic, 
    predicting better weather conditions the further into the future we look.
    - This could indicate that forecast models assume a more stable or favorable 
    weather trend in the long run, which might not always be accurate.
            
    **Implication:**
            
    If relying on long-term forecasts, expect actual weather conditions to be 
    slightly worse than initially predicted. This optimistic bias should be 
    considered when making plans based on extended forecasts.
            

    ✅ Temperature Trends:
    - The predicted temperature is lower at Day +5 compared to Day +1, 
    indicating a pessimistic bias in long-term forecasts.
    - As the forecast horizon shortens, temperature predictions tend to increase, 
    meaning that forecasts gradually adjust upward as the actual day approaches.
    - This suggests that initial long-term forecasts may systematically 
    underestimate temperatures, possibly due to conservative modeling assumptions.
    
    **Implication:**
            
    If relying on long-term forecasts, expect actual temperatures to be slightly 
    warmer than initially predicted. This bias should be considered when planning
    activities based on temperature forecasts several days in advance.    
        
            
    ✅ Rain Probability Trends:
    - Rain probability predictions decrease as the forecast horizon extends, 
    meaning that forecasts predict drier conditions at Day +5 compared to Day +1.
    - This suggests that forecast models might systematically underestimate 
    precipitation over time, possibly to avoid over-predicting rain in long-term 
    forecasts.
    - This optimistic bias means that long-term forecasts tend to underestimate 
    rainfall, even if actual conditions may differ.
            
    **Implication:**
            
    If relying on long-term forecasts, expect actual rain probabilities to be 
    slightly higher than initially predicted. It’s best to recheck forecasts 
    closer to the date to get a more accurate estimate.
            

    ✅ Humidity Trends:
    - Humidity forecasts fluctuate, peaking around Day +3 before declining, 
    suggesting instability in long-term predictions.
    - This variability indicates that humidity predictions become less reliable 
    over extended forecast horizons, likely due to increased uncertainty in 
    atmospheric moisture modeling.
    - The drop after Day +3 aligns with the decreasing rain probability trend, 
    possibly reflecting a systematic bias toward predicting drier conditions in 
    long-term forecasts.
            
    **Implication:**
            
    If relying on long-term forecasts, expect actual humidity levels to be more 
    variable than predicted. Forecast accuracy improves significantly closer to 
    the date.
    
            

    #### Conclusion:
            
    These insights strongly suggest that weather forecasts tend to be overly 
    optimistic over time.
    - Better weather is predicted at longer time horizons, as seen in the 
    increasing Weather Score.
    - Temperatures tend to be initially underestimated, with forecasts adjusting 
    them upward as the day approaches.
    - Rain probability is consistently underestimated in long-term forecasts, 
    making precipitation forecasts less reliable over extended periods.
    - Humidity predictions fluctuate and become less stable beyond Day +3, 
    reinforcing the uncertainty in long-term forecasts.
    
    This highlights a clear forecasting bias:
            
    Short-term forecasts are more reliable, while longer-term predictions tend 
    to assume more favorable weather than reality.
    Understanding this bias allows for better interpretation of weather 
    forecasts, helping to make more informed decisions—especially for travel, 
    outdoor events, or industries reliant on accurate weather data.
    
""")
st.write("---")















# Filtrer les données en fonction de la ville sélectionnée
city_data = all_data[all_data["Ville"] == selected_city]
st.markdown(f"<a name='city-{selected_city.lower().replace(' ', '-')}'></a>", unsafe_allow_html=True)

# Affichage des informations générales
st.markdown(f"## 🌆 {selected_city} - Weather Overview")
st.write(f"**Data from:** {city_data['Date'].min()} to {city_data['Date'].max()}")
#st.write(f"**Latitude:** {city_data['Latitude'].iloc[0]}")
#st.write(f"**Longitude:** {city_data['Longitude'].iloc[0]}")

# Calcul des statistiques
avg_temp = city_data["Temp_Avg_jour1"].mean()
max_temp = city_data["Temp_Max_jour1"].max()
min_temp = city_data["Temp_Min_jour1"].min()
avg_humidity = city_data["Humidity_jour1"].mean()
rain_prob = city_data["Rain_Probability_jour1"].mean()
weather_score = city_data["Weather_Score_jour1"].sum()
accuracy_score = city_accuracy[city_accuracy["Ville"] == selected_city]["Mean_Accuracy"].values[0]
# Valeur la plus fréquente dans la colonne Weather_jour1
weather = city_data["Weather_jour1"].mode().values[0]

# Affichage des stats
st.markdown("### 📊 Weather Statistics")
col20, col21, col23 = st.columns(3)
col20.metric("🌡️ Avg Temp", f"{avg_temp:.2f}°C")
col21.metric("🔥 Max Temp", f"{max_temp:.2f}°C")
col23.metric("❄️ Min Temp", f"{min_temp:.2f}°C")

col24, col25, col26 = st.columns(3)
col24.metric("💧 Humidity", f"{avg_humidity:.1f}%")
col25.metric("☔ Rain Prob", f"{rain_prob * 100:.1f}%")
col26.metric("📊 Weather Score", f"{weather_score}")

col27, col28, col29 = st.columns(3)
col27.metric("🎯 Accuracy", f"{accuracy_score:.2f}")
col28.metric("🌦️ Most Common Weather", f"{weather}")

# Appliquer une taille uniforme pour toutes les villes
city_data["Size"] = 5
# 📍 Carte interactive avec Plotly
st.markdown("### 🗺️ City Location")
fig_map = px.scatter_mapbox(
    city_data.groupby(["Ville", "Latitude", "Longitude"]).first().reset_index(),
    lat="Latitude",
    lon="Longitude",
    hover_name="Ville",
    mapbox_style="open-street-map",
    zoom=7,
    size="Size",
    size_max=10,
    color_discrete_sequence=["red"],
)
st.plotly_chart(fig_map)

st.markdown("### 📊 Weather Trends Over Time")
# Calcul du total de Weather_Score par jour
weather_score_daily = city_data.groupby("Date")["Weather_Score_jour1"].sum().reset_index()

# 📊 Graphique du score météo
fig_weather_score, ax = plt.subplots(figsize=(15, 8))
sns.lineplot(x=weather_score_daily["Date"], 
             y=weather_score_daily["Weather_Score_jour1"], 
             marker="o", 
             color="purple", 
             ax=ax,
             ci=None)

plt.xticks(rotation=90, fontsize=10, color="black")
plt.yticks(fontsize=10, color="black")
plt.title("Weather Score", fontsize=16, color="black", fontweight="bold")
plt.ylabel("Weather Score", fontsize=12, color="black", fontweight="bold")

# 📈 Graphique des températures
fig_temp, ax = plt.subplots(figsize=(15, 8))
sns.lineplot(
    x=city_data["Date"], 
    y=city_data["Temp_Avg_jour1"], 
    marker="o", 
    ci=None,
    linewidth=2,
    markersize=8,
    ax=ax)

plt.xticks(rotation=90, fontsize=10, color="black")
plt.yticks(fontsize=10, color="black")
plt.title("Temperature", fontsize=16, color="black", fontweight="bold")
plt.ylabel("Average Temperature (°C)", fontsize=12, color="black", fontweight="bold")

# 📊 Graphique des précipitations
fig_rain, ax = plt.subplots(figsize=(15, 8))
sns.lineplot(x=city_data["Date"], 
             y=city_data["Rain_Probability_jour1"], 
             marker="o", 
             color="blue", 
             ax=ax,
             ci=None
             )

plt.xticks(rotation=90, fontsize=10, color="black")
plt.yticks(fontsize=10, color="black")
plt.title("Rain Probability", fontsize=16, color="black", fontweight="bold")
plt.ylabel("Rain Probability (%)", fontsize=12, color="black", fontweight="bold")

# 📉 Graphique de l'humidité
fig_humidity, ax = plt.subplots(figsize=(15, 8))
sns.lineplot(x=city_data["Date"], 
             y=city_data["Humidity_jour1"], 
             marker="o", 
             color="green", 
             ax=ax,
             ci=None
             )

plt.xticks(rotation=90, fontsize=10, color="black")
plt.yticks(fontsize=10, color="black")
plt.title("Humidity", fontsize=16, color="black", fontweight="bold")
plt.ylabel("Humidity (%)", fontsize=12, color="black", fontweight="bold")

# Affichage des graphiques en 2 colonnes
col54, col55 = st.columns(2)
col54.pyplot(fig_weather_score)
col55.pyplot(fig_temp)

col56, col57 = st.columns(2)
col56.pyplot(fig_rain)
col57.pyplot(fig_humidity)


st.markdown("### 🎯 Optimistic or Pessimistic?")
# 📊 Calcul des statistiques spécifiques à la ville
weather_score_city = {
    "Day +1": city_data["Weather_Score_jour1"].mean(),
    "Day +2": city_data["Weather_Score_jour2"].mean(),
    "Day +3": city_data["Weather_Score_jour3"].mean(),
    "Day +4": city_data["Weather_Score_jour4"].mean(),
    "Day +5": city_data["Weather_Score_jour5"].mean(),
}
temp_avg_city = {
    "Day +1": city_data["Temp_Avg_jour1"].mean(),
    "Day +2": city_data["Temp_Avg_jour2"].mean(),
    "Day +3": city_data["Temp_Avg_jour3"].mean(),
    "Day +4": city_data["Temp_Avg_jour4"].mean(),
    "Day +5": city_data["Temp_Avg_jour5"].mean(),
}
rain_prob_city = {
    "Day +1": city_data["Rain_Probability_jour1"].mean(),
    "Day +2": city_data["Rain_Probability_jour2"].mean(),
    "Day +3": city_data["Rain_Probability_jour3"].mean(),
    "Day +4": city_data["Rain_Probability_jour4"].mean(),
    "Day +5": city_data["Rain_Probability_jour5"].mean(),
}
humidity_avg_city = {
    "Day +1": city_data["Humidity_jour1"].mean(),
    "Day +2": city_data["Humidity_jour2"].mean(),
    "Day +3": city_data["Humidity_jour3"].mean(),
    "Day +4": city_data["Humidity_jour4"].mean(),
    "Day +5": city_data["Humidity_jour5"].mean(),
}

# 📈 Fonction pour créer un lineplot amélioré
def create_lineplot(data, title, xlabel, ylabel, color):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(list(data.keys()), list(data.values()), marker="o", linestyle="-", color=color, linewidth=2)
    
    # Ajouter les valeurs sur les points
    for i, txt in enumerate(data.values()):
        ax.annotate(f"{txt:.2f}", (list(data.keys())[i], txt), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=10, fontweight="bold")

    
    ax.set_ylabel(ylabel, fontsize=12, fontweight="bold")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.grid(True)
    return fig

# 📊 Création des graphiques dynamiques pour la ville sélectionnée
fig_weather_city = create_lineplot(weather_score_city, f"Weather Score Evolution in {selected_city}", "Day", "Weather Score", "purple")
fig_temp_city = create_lineplot(temp_avg_city, f"Temperature Evolution in {selected_city}", "Day", "Average Temperature", "red")
fig_rain_city = create_lineplot(rain_prob_city, f"Rain Probability Evolution in {selected_city}", "Day", "Rain Probability", "blue")
fig_humidity_city = create_lineplot(humidity_avg_city, f"Humidity Evolution in {selected_city}", "Day", "Average Humidity", "green")

# Affichage des graphiques en 2 colonnes
col50, col51 = st.columns(2)
col50.pyplot(fig_weather_city)
col51.pyplot(fig_temp_city)

col52, col53 = st.columns(2)
col52.pyplot(fig_rain_city)
col53.pyplot(fig_humidity_city)


