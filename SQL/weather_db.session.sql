SELECT * FROM weather_forecast_1day LIMIT 10;

-- Compter le nombre de lignes dans chaque table
SELECT '1 Day', COUNT(*) FROM weather_forecast_1day
UNION ALL
SELECT '2 Days', COUNT(*) FROM weather_forecast_2day
UNION ALL
SELECT '3 Days', COUNT(*) FROM weather_forecast_3day
UNION ALL
SELECT '4 Days', COUNT(*) FROM weather_forecast_4day
UNION ALL
SELECT '5 Days', COUNT(*) FROM weather_forecast_5day;

-- Faire une jointure entre les tables
WITH weather_forecast AS (
    SELECT 
        d1.id,
        d1.ville,
        d1.latitude,
        d1.longitude,
        d1.date,
        d1.temp_min AS temp_min1,
        d1.temp_max AS temp_max1,
        d1.temp_avg AS temp_avg1,
        d1.humidity AS humidity1,
        d1.weather AS weather1,
        d1.rain_probability AS rain_risk1,
        d1.weather_score AS score1,
        d1.run_date AS date_collected
    FROM 
        weather_forecast_1day AS d1
    JOIN weather_forecast_2day AS d2 ON d1.date = d2.date AND d1.run_date = d2.run_date
    JOIN weather_forecast_3day AS d3 ON d1.date = d3.date AND d1.run_date = d3.run_date
    JOIN weather_forecast_4day AS d4 ON d1.date = d4.date AND d1.run_date = d4.run_date
    JOIN weather_forecast_5day AS d5 ON d1.date = d5.date AND d1.run_date = d5.run_date
)
SELECT * FROM weather_forecast LIMIT 10;
