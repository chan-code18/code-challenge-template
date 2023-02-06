CREATE DATABASE weather_challenge;  
USE weather_challenge;
CREATE TABLE weather_station (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  station_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  location TEXT NOT NULL
);

CREATE TABLE weather_data (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  station_id INTEGER NOT NULL,
  date TEXT NOT NULL,
  max_temp REAL NOT NULL,
  min_temp REAL NOT NULL,
  precipitation REAL NOT NULL,
  FOREIGN KEY (station_id) REFERENCES weather_station (id)
);
