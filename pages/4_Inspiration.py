import streamlit as st
import pandas as pd
import plotly.express as px
import random


# Fonction pour charger et préparer les données
def load_data():
    return pd.read_csv("final_results.csv")

# Charger les données
df = load_data()

# Titre de la page
st.markdown("# Inspiration")
st.markdown("### Choose your inspiration method and find your next adventure!")

# Choix de la méthode
method = st.radio(
    "How would you like to be inspired?",
    (
        "Filter by Preferences",
        "City with Best Weather Score and Temperature",
        "Random City"
    )
)

# Option 1 
if method == "Filter by Preferences":
    st.sidebar.markdown("### Customize Your Search")
    # Slider combiné pour Température (plage)
    temp_min, temp_max = st.sidebar.slider(
        "Select Temperature Range (°C)",  # Label du slider
        -10, 40,  # Valeurs minimale et maximale possibles
        (0, 25)  # Valeurs par défaut (plage initiale)
    )
    rain_min, rain_max = st.sidebar.slider(
        "Rain Probability Range (%)",
          0.0, 1.0, 
          (0.0, 0.5)
    )

    # Filtrer les données
    filtered_df = df[
        (df["Temp_Avg"] >= temp_min) &
        (df["Temp_Avg"] <= temp_max) &
        (df["Rain_Probability"] >= rain_min) &
        (df["Rain_Probability"] <= rain_max)
    ]

    # Trouver la meilleure ville pour chaque jour
    best_cities_per_day = (
        filtered_df.groupby("Date")
        .apply(lambda x: x.sort_values(by="Weather_Score", ascending=False).iloc[0])
        .reset_index(drop=True)
    )

    if not best_cities_per_day.empty:
        st.markdown("### Top Recommendations Based on Your Preferences")

        # liens cliquables pour l'hôtel
        def safe_hotel_link(row):
            if 'Hotel_1_Link' in row and pd.notna(row['Hotel_1_Link']) and row['Hotel_1_Link'] != 'N/A':
                return f"<a href='{row['Hotel_1_Link']}' target='_blank'>Book it!</a>"
            else:
                return "No hotel available"

        best_cities_per_day["Hotel"] = best_cities_per_day.apply(safe_hotel_link, axis=1)

        # liens cliquables pour les trains
        best_cities_per_day["Train"] = best_cities_per_day.apply(
            lambda row: f"<a href='{row['Train']}' target='_blank'>Let's Go</a>",
            axis=1
        )

        # Afficher le tableau
        st.markdown(
            best_cities_per_day[["Date", "Ville", "Temp_Avg", "Weather", "Rain_Probability", "Hotel", "Train"]]
            .to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

        # Carte
        st.markdown("### Explore on the Map")
        fig = px.scatter_mapbox(
            best_cities_per_day,
            lat="Latitude",
            lon="Longitude",
            hover_name="Ville",
            hover_data=["Temp_Avg", "Weather", "Rain_Probability"],
            mapbox_style="open-street-map",
            zoom=4
        )
        # Agrandir les points 
        fig.update_traces(marker=dict(size=15))
        fig.update_traces(marker=dict(color='blue'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("### No destinations match your criteria. Try adjusting the filters!")

# Option 2 
elif method == "City with Best Weather Score and Temperature":

    df["Global_Score"] = (
        df["Weather_Score"] * 0.5 +        # priorité météo
        df["Temp_Avg"] * 10 * 0.3 -        # chaleur agréable
        df["Rain_Probability"] * 100 * 0.2 # pénalité pluie
    )
    
    # Regrouper les données par Ville et Date
    daily_city_data = (
        df.groupby(["Ville", "Date"], as_index=False)
        .agg({
            "Weather_Score": "sum",
            "Temp_Avg": "mean",
            "Rain_Probability": "mean",
            "Weather": lambda x: x.mode()[0],  # météo la plus fréquente
            "Latitude": "first",
            "Longitude": "first",
            "Hotel_1_Link": "first",
            "Train": "first"
        })
)
    best_city = daily_city_data.sort_values(
        by=["Weather_Score", "Temp_Avg"], ascending= [False, False]).iloc[0]

    # Vérifier si le lien d'hôtel existe
    hotel_link = (
        best_city["Hotel_1_Link"]
        if "Hotel_1_Link" in best_city and pd.notna(best_city["Hotel_1_Link"]) and best_city["Hotel_1_Link"] != "N/A"
        else None
    )

    # Créer l'affichage avec ou sans le lien hôtel
    st.markdown(f"### Best Destination: **{best_city['Ville']}**")
    st.markdown(f"""
    - **Date**: {best_city['Date']}
    - **Average Temperature**: {best_city['Temp_Avg']}°C
    - **Weather**: {best_city['Weather']}
    - **Rain Probability**: {best_city['Rain_Probability']}%
    - **Hotel**: {'[Book it!](' + hotel_link + ')' if hotel_link else 'No hotel available'}
    - **Train**: [Let's Go!]({best_city['Train']})
    """)

    # Carte
    fig = px.scatter_mapbox(
        pd.DataFrame([best_city]),
        lat="Latitude",
        lon="Longitude",
        hover_name="Ville",
        mapbox_style="open-street-map",
        zoom=6,
    )
    # Agrandir les points
    fig.update_traces(marker=dict(size=15, color='blue'))
    #fig.update_traces(marker=dict(color='blue'))
    st.plotly_chart(fig, use_container_width=True)

# Option 3
elif method == "Random City":
    random_city = random.choice(df["Ville"].unique())
    city_data = df[df["Ville"] == random_city]

    # Regrouper par jour pour afficher une ligne par jour
    city_grouped_by_day = city_data.groupby("Date").first().reset_index()

    # liens cliquables pour l'hôtel
    def safe_hotel_link(row):
        if 'Hotel_1_Link' in row and pd.notna(row['Hotel_1_Link']) and row['Hotel_1_Link'] != 'N/A':
            return f"<a href='{row['Hotel_1_Link']}' target='_blank'>Book it!</a>"
        else:
            return "No hotel available"

    city_grouped_by_day["Hotel"] = city_grouped_by_day.apply(safe_hotel_link, axis=1)

    # liens cliquables pour les trains
    city_grouped_by_day["Train"] = city_grouped_by_day.apply(
        lambda row: f"<a href='{row['Train']}' target='_blank'>Let's Go</a>",
        axis=1
    )

    st.markdown(f"### Random Destination: **{random_city}**")
    st.markdown("#### Weather Highlights")

    # Afficher le tableau
    st.markdown(
        city_grouped_by_day[["Date", "Temp_Avg", "Weather", "Rain_Probability", "Hotel", "Train"]]
        .to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

    # Carte
    st.markdown("### Explore on the Map")
    fig = px.scatter_mapbox(
        city_grouped_by_day,
        lat="Latitude",
        lon="Longitude",
        hover_name="Ville",
        mapbox_style="open-street-map",
        zoom=6
    )
    # Agrandir les points
    fig.update_traces(marker=dict(size=15))
    fig.update_traces(marker=dict(color='blue'))
    st.plotly_chart(fig, use_container_width=True)
