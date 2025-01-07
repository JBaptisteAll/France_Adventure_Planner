import streamlit as st
import pandas as pd
import plotly.express as px



def load_data():
    df = pd.read_csv("final_results.csv")
    return df

# Affiche l'image avec une taille personnalisée
st.image("Assets/Logo_FAP.png", use_container_width=False, width=600)

# Custom title with larger font size
st.markdown("""<h1 style='text-align: center; font-size: 8em;'>
             Welcome 
            </h1>""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align: center; font-size: 3.5em;'>
    to the France Adventure Planner: Weather & Travel Insights 🌍
    </h1>""", unsafe_allow_html=True)

# Introduction
st.markdown("""
This application helps you explore and plan your adventures in France by providing accurate weather data and inspiring travel ideas.
Navigate through the sidebar to discover the following pages:
""")

# Load data
df = load_data()

# Since we have multiple forecasts for each city and multiple dates, let's just show current predictions or a subset.
# For demo, let's pick the first date available for each city.
df_unique = df.groupby("Ville").first().reset_index()

# Group the data
df_agg = df.groupby(["Ville", "Date", "Day_Time"], as_index=False).agg({
    "Temp_Max": "mean",
    "Temp_Min": "mean",
    "Temp_Avg": "mean",
    "Humidity": "mean",
    "Rain_Probability": "mean",
    "Weather": lambda x: x.mode()[0]
})

# Round Values for visibility
df_agg["Temp_Max"] = df_agg["Temp_Max"].round(1)
df_agg["Temp_Min"] = df_agg["Temp_Min"].round(1)
df_agg["Temp_Avg"] = df_agg["Temp_Avg"].round(1)
df_agg["Humidity"] = df_agg["Humidity"].round(1)
df_agg["Rain_Probability"] = df_agg["Rain_Probability"].round(1)

# Section : À Propos du Projet
st.markdown("## The Project")
st.markdown("""
This project combines my passion for travel and data analysis to create an application that helps users make smarter travel decisions. 
Planning a weekend getaway can be challenging, especially with unpredictable weather. 
This app makes it easier and more enjoyable to discover ideal destinations based on real-time weather data and user preferences. 
""")

# Objectif Principal
st.markdown("#### - Main Objective")
st.markdown("""
The goal is to provide users with personalized destination recommendations by analyzing weather conditions, so they can plan their trips effortlessly. 
""")


# Create a map figure with plotly
fig = px.density_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    z="Temp_Avg",
    mapbox_style="open-street-map",
    animation_frame="Date",
    zoom=3.5,
    radius=5,
    center={"lat": 46.603354, "lon": 1.888334},
    color_continuous_scale="Plasma"
)


# Affichage dans Streamlit
st.plotly_chart(fig, use_container_width=True)

# Page descriptions
st.markdown("#### - Key Features")
st.markdown("""
- **Mountains**: Discover the best trails and mountain adventures for your next hiking trip.
- **Sea & Sun**: Plan a relaxing weekend by the seaside with the latest weather updates.
- **Inspiration**: Let us guide you with hand-picked travel destinations.
- **Interactive Maps**: Visualize recommended destinations on dynamic maps with detailed weather insights.
- **Hotel Suggestions**: Get direct links to top-rated hotels in each destination for a hassle-free experience.            
""")


# Closing note
st.markdown("⬅️ Use the sidebar to start exploring. Enjoy your journey!")

# Fonctionnalités



# Valeur Ajoutée
st.markdown("#### - What Makes It Unique?")
st.markdown("""
This app combines weather data, data analysis, and interactive maps to create a seamless user experience. 
Its ability to recommend destinations based on personal preferences and current weather makes it stand out, 
offering both inspiration and practical tools for travel planning. ✨
""")

