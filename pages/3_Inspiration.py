import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Inspiration", page_icon="💡", layout="wide")

def load_data():
    df = pd.read_csv("final_results.csv")
    return df

st.markdown("## Inspiration")
st.markdown("Not sure where to go next weekend? Let us inspire you with a random suggestion from our list of destinations!")

df = load_data()
cities = df["Ville"].unique().tolist()
random_city = random.choice(cities)

st.markdown(f"**Random Suggested Destination:** {random_city}")

city_data = df[df["Ville"] == random_city].sort_values("Date")
st.dataframe(city_data[[
    "Date", "Temp_Avg", "Temp_Max", "Temp_Min", "Weather", "Rain_Probability", "Hotel_1_Name", "Hotel_1_Link"
]])
