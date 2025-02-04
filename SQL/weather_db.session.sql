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