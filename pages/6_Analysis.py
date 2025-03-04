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
- **Jour 2** → Weather forecast for two days ahead
- **Jour 3** → Weather forecast for three days ahead
- **Jour 4** → Weather forecast for four days ahead
- **Jour 5** → Weather forecast for five days ahead

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

gif_url = "https://github.com/JBaptisteAll/France_Adventure_Planner/blob/main/Assets/DataFlow.gif"
st.markdown(
    f'<img src="{gif_url}" width="300">',
    unsafe_allow_html=True
)
st.markdown("#### 01  ")
st.image("https://github.com/JBaptisteAll/France_Adventure_Planner/blob/main/Assets/DataFlow.gif")

st.markdown("#### 02  ")
st.image("Assets\DataFlow.gif", use_container_width=False, width=600)

st.markdown("#### 03  ")
st.components.v1.html(
    f'<img src="{gif_url}" width="300" style="display: block; margin: auto;">',
    height=300
)




st.markdown("# COMING SOON")
st.write(
    """This page will contain an analysis of the weather data that we have collected
    from the various cities in France. We will be using the data to provide
    accuracy scores for each city."""
)
