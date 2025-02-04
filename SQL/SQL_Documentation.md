# 🌤️ Weather Forecast Database Setup

## 📌 1. Database Overview
The weather forecast data is collected daily and stored in **five separate tables**, each representing the weather forecast for different prediction horizons:
- `weather_forecast_1day` → Forecast for **1 day ahead**
- `weather_forecast_2day` → Forecast for **2 days ahead**
- `weather_forecast_3day` → Forecast for **3 days ahead**
- `weather_forecast_4day` → Forecast for **4 days ahead**
- `weather_forecast_5day` → Forecast for **5 days ahead**

Each table will be used to **analyze and compare** the accuracy of forecasts over different days.

---

## 📌 2. Table Schema

Each table has the same structure:

```sql
CREATE TABLE weather_forecast_Xday (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ville TEXT,
    latitude REAL,
    longitude REAL,
    date DATE,
    temp_max REAL,
    temp_min REAL,
    humidity INTEGER,
    weather TEXT,
    rain_probability REAL CHECK (rain_probability >= 0 AND rain_probability <= 1),
    weather_score INTEGER,
    temp_avg REAL,
    run_date DATE
);
```
> 🔹 Replace `Xday` with `1day`, `2day`, `3day`, `4day`, or `5day`.

Each table contains:
- **`id`**: Auto-incremented primary key.
- **`ville`**: City name.
- **`latitude` / `longitude`**: GPS coordinates.
- **`date`**: Forecasted date.
- **`temp_max` / `temp_min`**: Maximum and minimum temperatures.
- **`humidity`**: Humidity percentage.
- **`weather`**: Description of the weather (e.g., *rainy, sunny, cloudy*).
- **`rain_probability`**: Probability of rain (between `0` and `1`).
- **`weather_score`**: Custom score for weather conditions.
- **`temp_avg`**: Average temperature.
- **`run_date`**: Date the forecast was generated.

---

## 📌 3. Importing Weather Data into SQLite

Each CSV file contains daily weather forecasts and is stored in the `/forecasts/` directory.

To import the data into its respective table, follow these steps:

### **1️⃣ Clean Temporary Table**
Before importing a new file, ensure that the temporary table is empty:
```sql
DELETE FROM temp_weather;
```

### **2️⃣ Import CSV into Temporary Table**
Run the following command to load the CSV file:
```sql
.import "C:/Insert/The/Path/To/Your/File/weather_data_forecast_Xday.csv" temp_weather
```
> 🔹 Replace `Xday` with the corresponding forecast day (`1day`, `2day`, etc.).

### **3️⃣ Remove Header Row**
Some CSV files might have headers. To avoid errors, remove them:
```sql
DELETE FROM temp_weather WHERE ville = 'Ville';
```

### **4️⃣ Handle Incorrect Values in `rain_probability`**
Ensure that rain probability values stay within the valid range (`0` to `1`):
```sql
UPDATE temp_weather SET rain_probability = NULL WHERE rain_probability < 0 OR rain_probability > 1;
```

### **5️⃣ Insert Data into the Correct Table**
Now, move the cleaned data from `temp_weather` into the correct table:
```sql
INSERT INTO weather_forecast_Xday (ville, latitude, longitude, date, temp_max, temp_min, humidity, weather, rain_probability, weather_score, temp_avg, run_date)
SELECT ville, latitude, longitude, date, temp_max, temp_min, humidity, weather, rain_probability, weather_score, temp_avg, run_date
FROM temp_weather;
```
> 🔹 Replace `Xday` accordingly.

### **6️⃣ Verify Data Import**
Check if the data has been inserted correctly:
```sql
SELECT COUNT(*) FROM weather_forecast_Xday;
```

---

## 📌 4. Importing All Forecast Days

Repeat the process for each forecast file (`1day.csv`, `2day.csv`, `3day.csv`, `4day.csv`, `5day.csv`) using the corresponding table (`weather_forecast_1day`, etc.).

### **Example for 2-Day Forecast**
```sql
DELETE FROM temp_weather;
.import "C:/Insert/The/Path/To/Your/File/weather_data_forecast_2day.csv" temp_weather
DELETE FROM temp_weather WHERE ville = 'Ville';
UPDATE temp_weather SET rain_probability = NULL WHERE rain_probability < 0 OR rain_probability > 1;

INSERT INTO weather_forecast_2day (ville, latitude, longitude, date, temp_max, temp_min, humidity, weather, rain_probability, weather_score, temp_avg, run_date)
SELECT ville, latitude, longitude, date, temp_max, temp_min, humidity, weather, rain_probability, weather_score, temp_avg, run_date
FROM temp_weather;
```
💚 **Repeat for `3day`, `4day`, and `5day`.**

---

## 📌 5. Verifying All Tables

Once all data is inserted, check the number of rows in each table:

```sql
SELECT '1 Day', COUNT(*) FROM weather_forecast_1day
UNION ALL
SELECT '2 Days', COUNT(*) FROM weather_forecast_2day
UNION ALL
SELECT '3 Days', COUNT(*) FROM weather_forecast_3day
UNION ALL
SELECT '4 Days', COUNT(*) FROM weather_forecast_4day
UNION ALL
SELECT '5 Days', COUNT(*) FROM weather_forecast_5day;
```

💚 If each table contains approximately **26,400 rows**, the import was **successful!** 🎉🚀  

---

# 🎯 **Next Steps**
With all forecast data properly stored in SQLite, we can now:
- Analyze weather patterns over multiple days.
- Compare forecast accuracy for different cities.
- Optimize weather predictions for **France Adventure Planner**.

---
