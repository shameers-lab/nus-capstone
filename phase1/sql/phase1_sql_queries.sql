-- Phase 1 SQL analysis for Metro Interstate Traffic Volume
-- Dataset: Metro_Interstate_Traffic_Volume.csv

-- 1. Inspect the table structure
SELECT *
FROM traffic_volume
LIMIT 10;

-- 2. Basic traffic summary
SELECT
    COUNT(*) AS total_records,
    MIN(traffic_volume) AS min_traffic,
    MAX(traffic_volume) AS max_traffic,
    AVG(traffic_volume) AS avg_traffic,
    ROUND(AVG(traffic_volume), 2) AS avg_traffic_rounded
FROM traffic_volume;

-- 3. Traffic by hour of the day
SELECT
    CAST(strftime('%H', date_time) AS INTEGER) AS hour_of_day,
    AVG(traffic_volume) AS avg_traffic,
    MAX(traffic_volume) AS max_traffic,
    MIN(traffic_volume) AS min_traffic
FROM traffic_volume
GROUP BY CAST(strftime('%H', date_time) AS INTEGER)
ORDER BY hour_of_day;

-- 4. Traffic by day of week
SELECT
    CASE
        WHEN CAST(strftime('%w', date_time) AS INTEGER) = 0 THEN 'Sunday'
        WHEN CAST(strftime('%w', date_time) AS INTEGER) = 1 THEN 'Monday'
        WHEN CAST(strftime('%w', date_time) AS INTEGER) = 2 THEN 'Tuesday'
        WHEN CAST(strftime('%w', date_time) AS INTEGER) = 3 THEN 'Wednesday'
        WHEN CAST(strftime('%w', date_time) AS INTEGER) = 4 THEN 'Thursday'
        WHEN CAST(strftime('%w', date_time) AS INTEGER) = 5 THEN 'Friday'
        ELSE 'Saturday'
    END AS weekday,
    AVG(traffic_volume) AS avg_traffic
FROM traffic_volume
GROUP BY weekday
ORDER BY CASE weekday
    WHEN 'Monday' THEN 1
    WHEN 'Tuesday' THEN 2
    WHEN 'Wednesday' THEN 3
    WHEN 'Thursday' THEN 4
    WHEN 'Friday' THEN 5
    WHEN 'Saturday' THEN 6
    ELSE 7
END;

-- 5. Holiday vs non-holiday traffic
SELECT
    holiday,
    COUNT(*) AS records,
    AVG(traffic_volume) AS avg_traffic,
    MAX(traffic_volume) AS max_traffic
FROM traffic_volume
GROUP BY holiday
ORDER BY avg_traffic DESC;

-- 6. Weather influence on traffic
SELECT
    weather_main,
    AVG(traffic_volume) AS avg_traffic,
    COUNT(*) AS records
FROM traffic_volume
GROUP BY weather_main
ORDER BY avg_traffic DESC;

-- 7. Monthly traffic trend
SELECT
    CAST(strftime('%m', date_time) AS INTEGER) AS month_number,
    AVG(traffic_volume) AS avg_traffic
FROM traffic_volume
GROUP BY month_number
ORDER BY month_number;

-- 8. Traffic comparison during rain and clear weather
SELECT
    CASE
        WHEN rain_1h > 0 THEN 'Rain'
        ELSE 'No Rain'
    END AS rain_flag,
    AVG(traffic_volume) AS avg_traffic,
    COUNT(*) AS records
FROM traffic_volume
GROUP BY rain_flag;

-- 9. Peak traffic by weather type
SELECT
    weather_main,
    MAX(traffic_volume) AS peak_traffic,
    AVG(traffic_volume) AS avg_traffic
FROM traffic_volume
GROUP BY weather_main
ORDER BY peak_traffic DESC;

-- 10. High-traffic condition query
SELECT *
FROM traffic_volume
WHERE traffic_volume > 7000
ORDER BY traffic_volume DESC
LIMIT 20;

-- 11. Example conditional analysis
SELECT
    COUNT(*) AS total_records,
    SUM(CASE WHEN rain_1h > 0 AND traffic_volume > 5000 THEN 1 ELSE 0 END) AS rain_high_traffic,
    AVG(CASE WHEN rain_1h > 0 THEN traffic_volume END) AS avg_traffic_rain,
    AVG(CASE WHEN rain_1h = 0 THEN traffic_volume END) AS avg_traffic_no_rain
FROM traffic_volume;

-- Notes:
-- Continue with additional SQL queries as needed for the final capstone analysis.
-- All SQL should be documented and explained in the final written report.
