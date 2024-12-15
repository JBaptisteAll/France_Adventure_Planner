import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trek & Mountains", page_icon="⛰️", layout="wide")

def load_data():
    df = pd.read_csv("final_results.csv")
    return df

# Example known treks:
treks = {
    "Les Ecrins": ["Bourg d'Oisans", "Le Périer", "La Chapelle-en-Valgaudémar", "Vallouise", "Ailefroide", "Monêtier-les-Bains", "La Grave", "Saint-Christophe-en-Oisans"],
    "Mont-Blanc": ["Chamonix", "Les Houches", "Les Co"]
}

st.markdown("## Trek & Mountains")
st.markdown("Select a known trek/hike itinerary and explore its weather forecasts and nearby accommodations.")

df = load_data()

chosen_trek = st.selectbox("Choose a Trek Itinerary", list(treks.keys()))

selected_cities = treks[chosen_trek]

st.markdown(f"**Selected Trek:** {chosen_trek}")
st.markdown(f"**Cities Involved:** {', '.join(selected_cities)}")

