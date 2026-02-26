# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

**France Adventure Planner** is a Streamlit web app that helps Parisians find ideal weekend getaway destinations based on real-time 5-day weather forecasts. It covers ~200 French cities across mountain ranges (Alps, Pyrenees, Jura), coastlines, and major cities, pairing weather data with hotel links scraped from Booking.com.

## Commands

```bash
# Install dependencies (run from project root)
pip install -r requirements.txt
pip install scrapy python-dotenv   # not in requirements.txt but needed for ETL

# Run ETL pipeline (requires API_KEY in .env)
python Weekend_getaway_project.py

# Launch the Streamlit app
streamlit run App.py

# Manual git push helper (legacy)
python auto_github.py
```

## Architecture

### Data Flow
```
Nominatim API (coords) ──┐
OpenWeatherMap API        ├──► Weekend_getaway_project.py ──► final_results.csv ──► Streamlit pages
Booking.com (Scrapy)  ───┘                                 └──► forecasts/weather_data_forecast_Nday.csv
```

**`Weekend_getaway_project.py`** — single-file ETL that runs in sequence:
1. Fetches lat/lon for each city from Nominatim (with 1-second rate-limit sleep)
2. Fetches 5-day/3-hour forecasts from OpenWeatherMap; maps weather descriptions to a custom `Weather_Score` (sunny = high positive int, storms/snow = negative)
3. Runs a Scrapy spider (`BookingSpider`) to scrape up to 5 hotels per city from Booking.com
4. Joins weather + hotel data → writes `final_results.csv`
5. Splits a subset of 50 cities into per-day forecast CSVs (`forecasts/weather_data_forecast_Nday.csv`) using **append** mode (historical accumulation)

**`App.py`** — defines Streamlit multi-page navigation; all pages are in `pages/`:

| Page file | Purpose |
|---|---|
| `1_Welcome.py` | Animated density heatmap of France temperature |
| `2_Mountains.py` | Trek picker (Alps/Pyrenees/Jura) with per-city forecast table + hotel links |
| `3_Sea_&_Sun.py` | Coastal destinations weather |
| `4_Inspiration.py` | Random destination suggestions |
| `5_About_Me.py` | Portfolio page |
| `6_Analysis.py` | Weather forecast accuracy analysis (reads from `Analyse_Bloc_6_CDSD/forecasts/`) |

All pages load data with `pd.read_csv("final_results.csv")` directly (no caching applied — `@st.cache_data` is commented out).

**`Analyse_Bloc_6_CDSD/`** — Jupyter notebooks and a separate `forecasts/` subfolder used by the Analysis page. This is a historical dataset distinct from the live `forecasts/` folder.

### GitHub Actions Automation
- **Schedule**: daily at 21:30 UTC (`.github/workflows/run_script.yml`)
- **Secret required**: `API_KEY` (OpenWeatherMap) must be set in GitHub repo secrets
- Commits only `final_results.csv` and `forecasts/` back to `main`

### Key Data Columns in `final_results.csv`
`Ville, Latitude, Longitude, Date, Hour, Day_Time, Temp_Max, Temp_Min, Temp_Avg, Humidity, Weather, Weather_Score, Rain_Probability, Run_Date, Hotel_1_Name … Hotel_5_Name, Hotel_1_Link … Hotel_5_Link, Train`

`Day_Time` is bucketed: Morning (6–12), Afternoon (12–18), Evening (18–22), Night.

### Windows-specific note
The ETL script forces `WindowsSelectorEventLoopPolicy` at the top to avoid Scrapy/asyncio conflicts on Windows. This is already handled; don't remove it.

## Local Development

- Copy `.env.example` (or create `.env`) with `API_KEY=<your_openweathermap_key>`
- The `requirements.txt` is missing `scrapy` and `python-dotenv` — install them separately
- Streamlit theme is dark (Solarized-dark palette) defined in `.streamlit/config.toml`
- The app must be run from the project root so relative paths (`final_results.csv`, `Assets/`) resolve correctly
