USE weather_challenge;
CREATE TABLE weather_stats (
    id SERIAL PRIMARY KEY,
    year INT NOT NULL,
    station_id VARCHAR(255) NOT NULL,
    avg_max_temp NUMERIC(10, 2) NULL,
    avg_min_temp NUMERIC(10, 2) NULL,
    total_precipitation NUMERIC(10, 2) NULL
);

INSERT INTO weather_stats (year, station_id, avg_max_temp, avg_min_temp, total_precipitation)
SELECT
    YEAR(date) AS year,
    station_id,
    AVG(IFNULL(max_temp, 0)) AS avg_max_temp,
    AVG(IFNULL(min_temp, 0)) AS avg_min_temp,
    SUM(IFNULL(precipitation, 0)) AS total_precipitation
FROM
    weather_data
WHERE max_temp != -9999 AND min_temp != -9999
GROUP BY
    YEAR(date), station_id;
