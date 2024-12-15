import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="France Adventure Planner: Weather & Travel Insights",
    page_icon="🌤️",
    layout="wide"
)

def load_data():
    df = pd.read_csv("final_results.csv")
    return df

# Custom title with larger font size
st.markdown("""
    <h1 style='text-align: center; font-size: 3.5em;'>
    Welcome to the Weather & Travel Explorer 🌍
    </h1>
    """, unsafe_allow_html=True)

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


# Create a map figure with plotly
fig = px.density_mapbox(
    df_unique,
    lat="Latitude",
    lon="Longitude",
    z="Temp_Avg",
    mapbox_style="open-street-map",
    zoom=4,
    radius=10,
    center={"lat": 46.603354, "lon": 1.888334},
    color_continuous_scale="Plasma"
)

# Affichage dans Streamlit
st.plotly_chart(fig, use_container_width=True)

# Page descriptions
st.markdown("""
- **Mountains**: Discover the best trails and mountain adventures for your next hiking trip.
- **Sea & Sun**: Plan a relaxing weekend by the seaside with the latest weather updates.
- **Inspiration**: Let us guide you with hand-picked travel destinations.
- **About Me**: Learn more about the creator behind this project.
""")

# Closing note
st.markdown("⬅️ Use the sidebar to start exploring. Enjoy your journey!")
