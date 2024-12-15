import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sea & Sun", page_icon="🏖️", layout="wide")

def load_data():
    df = pd.read_csv("final_results.csv")
    return df

# Assign cities to regions (example)
regions = {
    "Méditerranée": [],
    "Aquitaine": [],
    "Bretagne": [], 
    "Nord": []
}

st.markdown("## Sea & Sun")
st.markdown("Choose a coastal region and see weather forecasts and hotel suggestions for famous beach destinations.")

df = load_data()

chosen_region = st.selectbox("Choose a Coastal Region", list(regions.keys()))

selected_cities = regions[chosen_region]

st.markdown(f"**Selected Region:** {chosen_region}")
st.markdown(f"**Cities Involved:** {', '.join(selected_cities)}")


