Created the Database with SQLite

```pgsql
sqlite3 weather_data.db
```
---
Cretated the table

```sql
CREATE TABLE weather_forecast (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ville TEXT,
    latitude REAL,
    longitude REAL,
    date DATE,
    temp_max REAL,
    temp_min REAL,
    humidity INTEGER,
    weather TEXT,
    rain_probability REAL CHECK(rain_probability >= 0 AND rain_probability <= 1),
    weather_score INTEGER,
    temp_avg REAL,
    run_date DATE
);
```

Checked the table was successfully created
```sql
.tables
```

then ```weather_forecast``` should appear

---
activate CSV mode in SQLite
```sql
.mode csv
```

Import csv files

```sql
.import weather_data_forecast_1day.csv weather_forecast
```
