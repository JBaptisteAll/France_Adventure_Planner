# France_Adventure_Planner


## Overview
This project started as a simple data collection process to analyze weather trends over time. As I gathered more data, I saw an opportunity to turn it into something more useful: an application designed for Parisians looking for the best weekend getaway destinations based on real-time weather conditions.

The core idea is to help users discover ideal travel spots based on weather forecasts, with a strong focus on mountain destinations. Over time, the project expanded to include coastal regions and general inspiration for spontaneous travelers.

## Technologies Used
This project integrates multiple technologies:

- **Python**: Core language for data processing and scraping.
- **Streamlit**: For building the interactive web application.
- **Scrapy**: For scraping hotel recommendations.
- **OpenWeatherMap API**: To fetch weather forecast data.
- **Nominatim API**: To retrieve latitude and longitude of cities.
- **Pandas**: For data manipulation and analysis.
- **Plotly**: For visualizing weather conditions.
- **Make.com**: Automates the "Contact Me" form, storing user data in Google Sheets and sending automated email responses.
- **Windows Task Scheduler**: Automates script execution daily at 10:30 PM, followed by a second script that pushes the updated CSV files to GitHub.

## How It Works

1️⃣ **Automated Updates** → Task Scheduler runs scripts every night 

2️⃣ **Data Collection** → Weather & Hotel data are fetched via APIs and Scrapy   

3️⃣ **Data Storage** → Results are stored in `final_results.csv` 

4️⃣ **Visualization** → The Streamlit app displays the latest weather insights  

5️⃣ **User Interaction** → Contact form automates responses via Make.com  

## Data Collection Process

### 1. Weather Data Retrieval
- The script fetches weather data from **OpenWeatherMap API**.
- It retrieves forecasts for multiple cities and stores the results.
- Each forecast includes:
  - **Date and Time**
  - **Temperature (Max, Min, and Average)**
  - **Humidity**
  - **Weather conditions**
  - **Rain probability**
  - **Weather Score** (a custom rating based on predefined conditions)
- The data is stored in a structured CSV file for further analysis.

Additionally, I store **weather data for 50 specific cities in 5 separate CSV files** for future analysis.

### 2. Hotel Data Scraping
I implemented a **Scrapy** spider to collect hotel information from **Booking.com**:

- For each city, the scraper retrieves up to **5 hotels**.
- The extracted information includes:
  - **Hotel Name**
  - **Direct Booking Link**
- Scrapy uses a **custom user-agent** to prevent blocking and ensures polite crawling practices.
- The results are integrated into the main CSV file alongside the weather data.

## Data Storage and Structure
The main dataset is stored in `final_results.csv`, containing:

- **City (Ville)**: Name of the destination.
- **Latitude & Longitude**: Coordinates fetched via Nominatim API.
- **Date**: Forecast date.
- **Time of the day**: Categorized as Morning, Afternoon, Evening, or Night.
- **Temperature (Max, Min, Avg)**: Recorded for each forecast period.
- **Humidity**: Captures moisture levels.
- **Weather Description**: Text-based weather conditions.
- **Rain Probability**: Indicates chances of precipitation.
- **Weather Score**: A custom metric for ranking destinations based on weather quality.
- **Hotels**: Top 5 recommended hotels for each location, including names and booking links.

Additional CSV files store data for **50 specific cities** across different weather conditions for later analysis.

## Application Development
### 1. Streamlit Interface
The application is divided into multiple sections:
- **Welcome Page**: Overview and user guidance.
- **Mountains Page**: Focuses on hiking and trekking destinations.
- **Sea & Sun Page**: Highlights coastal areas for relaxation.
- **Inspiration Page**: Suggests random destinations for spontaneous trips.

Each page fetches data from `final_results.csv` and provides weather insights and hotel recommendations.

### 2. Interactive Features
- **Plotly Maps**: Visualizes temperature variations across destinations.
- **Dynamic Data Selection**: Users can filter destinations based on conditions.
- **Automated Contact Form**: Users can submit inquiries, with responses handled via Make.com automation.

## Key Takeaways
- ✅ **Data Collection & Processing**: Web scraping, API calls, data wrangling  
- ✅ **Web App Development**: Interactive UI with Streamlit & Plotly  
- ✅ **Automation & Deployment**: Windows Task Scheduler, Make.com integration  
- ✅ **Problem-Solving Mindset**: Pivoting from simple weather analysis to a full-scale app  

## Future Improvements
- **Paris Activities Page**: Add a dedicated section for users who prefer to stay in Paris, offering recommendations for cultural events, outdoor activities, and exhibitions happening in the city.  
- **Weather Data Analysis Page**: Introduce a new page focused on analyzing collected weather data, including trends, comparisons over time, and key insights to better understand how weather conditions evolve.  
- **Winter Travel Section**: : Develop a dedicated section for winter getaways, including ski resort recommendations, snowfall tracking, and ideal conditions for winter sports enthusiasts. 


## Conclusion
This project showcases my ability to **gather, clean, analyze, and visualize data**, as well as build an interactive web application. By combining real-time weather insights with web scraping and automation, I created a practical tool for travelers looking for optimal weekend destinations.

The project remains open for further improvements, including deeper data analysis and expanded features tailored for urban users seeking local activities.
