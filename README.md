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
- **GitHub Actions**: Automates script execution and data updates every day at 22:00 UTC.

## How It Works

1️⃣ **Automated Updates** → **GitHub Actions** runs scripts every night  

2️⃣ **Data Collection** → Weather & Hotel data are fetched via APIs and Scrapy   

3️⃣ **Data Storage** → Results are stored in `final_results.csv` and committed to GitHub  

4️⃣ **Visualization** → The Streamlit app displays the latest weather insights  

5️⃣ **User Interaction** → Contact form automates responses via Make.com  

Initially, Windows Task Scheduler was used during the first month to ensure that the script executed correctly and that the data updates were stable. Once the workflow proved to be reliable, the setup was migrated to GitHub Actions for full automation.

This new setup ensures seamless automation without requiring manual intervention or local execution. GitHub Actions replaces Windows Task Scheduler, allowing the script to run directly in the cloud and update data automatically every day.

---

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

| Column Name         | Description |
|---------------------|-------------|
| **City (Ville)**   | Destination name |
| **Latitude & Longitude** | Coordinates fetched via Nominatim API |
| **Date**           | Forecast date |
| **Time of the day** | Categorized as Morning, Afternoon, Evening, or Night |
| **Temperature (Max, Min, Avg)** | Temperature at different times of the day |
| **Humidity**       | Captures moisture levels |
| **Weather Description** | Text-based weather conditions |
| **Rain Probability** | Indicates chances of precipitation |
| **Weather Score**  | A custom metric for ranking destinations |
| **Hotels**         | Top 5 recommended hotels with booking links |

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

## 🔄 Automation & Deployment

✅ **Before**: Windows Task Scheduler ran scripts daily at 22:30 UTC, and a second script pushed the updated CSV files to GitHub.  
✅ **Now**: GitHub Actions **automatically runs the script every day at 22:00 UTC**, updates the dataset, and commits the changes to the repository.

### ✨ **What’s new with GitHub Actions?**
- **Cloud-based execution** → No need for a local machine.
- **Automated updates** → No manual intervention required.
- **Scheduled runs** → Script runs **every day at 22:00 UTC**.
- **GitHub-Integrated Logging** → Monitor execution directly in the **GitHub Actions dashboard**.


This **upgrade makes the project fully autonomous** and ensures up-to-date data for the Streamlit application.

---


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

With the upgrade to **GitHub Actions**, the project is now **fully automated**, ensuring up-to-date weather data without any manual intervention.


The project remains open for further improvements, including deeper data analysis and expanded features tailored for urban users seeking local activities.
