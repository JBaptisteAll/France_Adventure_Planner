import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Weather Analysis", page_icon="📊")


# Titre de la page
st.markdown("""<h1 style='text-align: center; font-size: 7em;'>
             Data Analysis 
            </h1>""", unsafe_allow_html=True)

st.write(
    """The France Adventure Planner project is based on collecting and analysing weather 
    and hotel data to help Parisians choose the best weekend destination based on 
    real-time weather conditions. """
)

st.write(
    """Explanation of the Data for This Analysis
To evaluate the reliability of weather forecasts across France, I collected meteorological 
data for 50 cities from a larger dataset of 250 locations. The data was recorded over 
a two-month period from December 5, 2024, to February 7, 2025, and was structured into 
5 separate files, each corresponding to a different forecast horizon:
- **Jour 1** → Weather forecast for the next day
- **Jour 2** → Weather forecast for the second day ahead
- **Jour 3** → Weather forecast for the third day ahead
- **Jour 4** → Weather forecast for the fourth day ahead
- **Jour 5** → Weather forecast for the fifth day ahead

This segmentation allows for a detailed comparison of forecast accuracy over time, 
helping to identify which locations have the most reliable weather predictions in France.
"""
)

st.markdown("#### - Data Sources")
st.markdown("""
- **OpenWeatherMap API **: Provides detailed weather forecasts (temperature, weather conditions, rain probability, etc)
- **Nominatim API**: Retrieves Latitude & Longitude coordinates for selected cities.
- **Scrapy (Web Scraping)**: Extracts hotel recommendations from Booking.com.
- **GitHub Actions**: Automates the script execution to update data daily.
""")

st.markdown("#### - Data collection flow")
# Affiche l'image
st.image("Assets/DataFlow.png", use_container_width=False, width=600)








st.markdown("# 🚧 Page Under Construction 🚧")
st.write(
    """I am currently working on analyzing the weather data collected from 
    various cities across France. This section will soon be available with 
    accuracy metrics and other valuable insights.  
    Stay tuned! ⏳"""
)
