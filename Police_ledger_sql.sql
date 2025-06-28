SELECT * FROM traffic_data

--- What are the top 10 vehicle_Number involved in drug-related stops?
SELECT vehicle_number FROM traffic_data Where drugs_related_stop = true LIMIT 10;

--- What is the gender distribution of drivers stopped in each country?
SELECT country_name, driver_gender, COUNT(*) AS total_stops
FROM traffic_data
GROUP BY country_name, driver_gender ORDER BY country_name, driver_gender;


-- Which race and gender combination has the highest search rate?

SELECT 
    driver_race,
    driver_gender,
    -- COUNT(*) AS total_stops,
    -- COUNT(*) FILTER (WHERE search_conducted = true) AS search_count,
    ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted = true) / COUNT(*), 2) AS search_rate_percent
FROM 
    traffic_data
GROUP BY
    driver_race, driver_gender
ORDER BY 
    search_rate_percent DESC
LIMIT 1;

--- Which driver age group had the highest arrest rate?

SELECT
    CASE
        WHEN driver_age < 18 THEN 'Under 18'
        WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
        WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
        WHEN driver_age BETWEEN 36 AND 50 THEN '36-50'
        WHEN driver_age BETWEEN 51 AND 65 THEN '51-65'
        ELSE '65+'
    END AS age_group,
    COUNT(*) FILTER (WHERE is_arrested = true) AS arrest_count,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_arrested = true) / COUNT(*), 2) AS arrest_rate_percent
FROM
    traffic_data
WHERE
    driver_age IS NOT NULL
GROUP BY
    age_group
ORDER BY
    arrest_rate_percent DESC
LIMIT 1;

-- Which vehicles were most frequently searched?
SELECT vehicle_number, COUNT(*) AS total_stops FROM traffic_data GROUP BY vehicle_number
ORDER BY total_stops DESC

-- Which violations are most associated with searches or arrests?
SELECT violation,
ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted = true or is_arrested = true) / COUNT(*), 2) AS search_or_arrest_percent 
FROM traffic_data
GROUP BY violation
ORDER BY search_or_arrest_percent DESC;

SELECT 
    violation,
    COUNT(*) AS total_stops,
    COUNT(*) FILTER (WHERE search_conducted = true) AS search_count,
    COUNT(*) FILTER (WHERE is_arrested = true) AS arrest_count,
    COUNT(*) FILTER (WHERE search_conducted = true OR is_arrested = true) AS search_or_arrest_count,
    ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted = true) / COUNT(*), 2) AS search_rate_percent,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_arrested = true) / COUNT(*), 2) AS arrest_rate_percent,
    ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted = true OR is_arrested = true) / COUNT(*), 2) AS search_or_arrest_percent
FROM 
    traffic_data
GROUP BY 
    violation
ORDER BY 
    search_or_arrest_percent DESC;

--- What time of day sees the most traffic stops?
SELECT 
    CASE
        WHEN hour >= 0 AND hour < 1 THEN '12-1 AM'
        WHEN hour >= 1 AND hour < 2 THEN '1-2 AM'
        WHEN hour >= 2 AND hour < 3 THEN '2-3 AM'
        WHEN hour >= 3 AND hour < 4 THEN '3-4 AM'
        WHEN hour >= 4 AND hour < 5 THEN '4-5 AM'
        WHEN hour >= 5 AND hour < 6 THEN '5-6 AM'
        WHEN hour >= 6 AND hour < 7 THEN '6-7 AM'
        WHEN hour >= 7 AND hour < 8 THEN '7-8 AM'
        WHEN hour >= 8 AND hour < 9 THEN '8-9 AM'
        WHEN hour >= 9 AND hour < 10 THEN '9-10 AM'
        WHEN hour >= 10 AND hour < 11 THEN '10-11 AM'
        WHEN hour >= 11 AND hour < 12 THEN '11-12 PM'
        WHEN hour >= 12 AND hour < 13 THEN '12-1 PM'
        WHEN hour >= 13 AND hour < 14 THEN '1-2 PM'
        WHEN hour >= 14 AND hour < 15 THEN '2-3 PM'
        WHEN hour >= 15 AND hour < 16 THEN '3-4 PM'
        WHEN hour >= 16 AND hour < 17 THEN '4-5 PM'
        WHEN hour >= 17 AND hour < 18 THEN '5-6 PM'
        WHEN hour >= 18 AND hour < 19 THEN '6-7 PM'
        WHEN hour >= 19 AND hour < 20 THEN '7-8 PM'
        WHEN hour >= 20 AND hour < 21 THEN '8-9 PM'
        WHEN hour >= 21 AND hour < 22 THEN '9-10 PM'
        WHEN hour >= 22 AND hour < 23 THEN '10-11 PM'
        WHEN hour >= 23 AND hour < 24 THEN '11-12 AM'
        ELSE 'Unknown'
    END AS hour_range,
    COUNT(*) AS stop_count
FROM (
    SELECT EXTRACT(HOUR FROM stop_time) AS hour
    FROM traffic_data
) AS sub
GROUP BY hour_range
ORDER BY stop_count DESC
LIMIT 1;

--- Are stops during the night more likely to lead to arrests?
SELECT 
	ROUND (100 * COUNT(*) FILTER (WHERE EXTRACT(HOUR FROM stop_time) >= 18 OR EXTRACT(HOUR FROM stop_time) < 6 )/ COUNT(*), 2) AS night_time,
	ROUND (100 * COUNT(*) FILTER (WHERE EXTRACT(HOUR FROM stop_time) >= 6 AND EXTRACT(HOUR FROM stop_time) < 18)/ COUNT(*), 2) AS day_time
FROM traffic_data
WHERE is_arrested = TRUE

SELECT 
    ROUND(100.0 * COUNT(*) FILTER (
        WHERE is_arrested = TRUE AND EXTRACT(HOUR FROM stop_time) >= 18 OR EXTRACT(HOUR FROM stop_time) < 6
    ) / COUNT(*), 2) AS night_time_percentage,

    ROUND(100.0 * COUNT(*) FILTER (
        WHERE is_arrested = TRUE AND EXTRACT(HOUR FROM stop_time) >= 6 OR EXTRACT(HOUR FROM stop_time) < 18
    ) / COUNT(*), 2) AS day_time_percentage
FROM traffic_data;

--- What is the average stop duration for different violations?
SELECT 
    violation,
    ROUND(AVG(
        CASE TRIM (stop_duration)
            WHEN '0-15 Min' THEN 7.5
            WHEN '15-30 Min' THEN 22.5
            WHEN '30+ Min' THEN 35
            ELSE NULL
        END
    ), 2) AS avg_stop_duration_minutes
FROM traffic_data
WHERE TRIM(stop_duration) IN ('0-15 Min', '15-30 Min', '30+ Min')
GROUP BY violation
ORDER BY avg_stop_duration_minutes DESC;

--- Which violations are most common among younger drivers (<25)?
SELECT violation, ROUND(100.0 * COUNT(*) FILTER (WHERE driver_age < 25)/ COUNT(*), 2) AS rate 
FROM traffic_data
GROUP BY violation
ORDER BY rate DESC;

--- Is there a violation that rarely results in search or arrest?
SELECT violation,
ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted = false AND is_arrested = false) / COUNT(*), 2) AS not_search_or_arrest_percent 
FROM traffic_data
GROUP BY violation
ORDER BY not_search_or_arrest_percent DESC;

--- Which countries report the highest rate of drug-related stops?
SELECT country_name,
ROUND(100.0 * COUNT(*) FILTER (WHERE drugs_related_stop = true) / COUNT(*), 2) AS drugs_related_stops
FROM traffic_data
GROUP BY country_name
ORDER BY drugs_related_stops DESC;

--- What is the arrest rate by country and violation?
SELECT 
    country_name,
    violation,
    ROUND(100.0 * SUM(CASE WHEN is_arrested = true THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent
FROM 
    traffic_data
GROUP BY 
    country_name, violation
ORDER BY 
    arrest_rate_percent DESC;

--- Which country has the most stops with search conducted?
SELECT country_name,
ROUND(100.0 * COUNT(*) FILTER(WHERE search_conducted = true) / COUNT(*), 2) AS search_rate
FROM traffic_data
GROUP BY country_name
ORDER BY search_rate DESC;

--- Top 5 Violations with Highest Arrest Rates
SELECT 
    violation,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_arrested = true) / COUNT(*), 2) AS arrest_rate_percent
FROM traffic_data
GROUP BY violation
ORDER BY arrest_rate_percent DESC;

--- Driver Demographics by Country (Age, Gender, and Race)
SELECT 
    country_name,
    driver_gender,
    driver_race,
    CASE 
        WHEN driver_age BETWEEN 16 AND 25 THEN '16-25'
        WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
        WHEN driver_age BETWEEN 36 AND 45 THEN '36-45'
        WHEN driver_age BETWEEN 46 AND 60 THEN '46-60'
        ELSE '60+'
    END AS age_group,
    COUNT(*) AS total_stops
FROM 
    traffic_data
WHERE 
    driver_age IS NOT NULL
GROUP BY 
    country_name, driver_gender, driver_race, age_group
ORDER BY 
    country_name, age_group, total_stops DESC;

--- Yearly Breakdown of Stops and Arrests by Country (Using Subquery and Window Functions)
SELECT 
RANK() OVER (
        PARTITION BY year 
        ORDER BY total_arrests DESC
    ) AS arrest_rank_in_year,
    country_name,
    year,
	total_stops,
	total_arrests,
    ROUND(100.0 * total_arrests / NULLIF(total_stops, 0), 2) AS arrest_rate_percent
FROM (
    SELECT
        country_name,
        EXTRACT(YEAR FROM stop_date)::INT AS year,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END) AS total_arrests
    FROM traffic_data
    GROUP BY country_name, year
) sub
ORDER BY arrest_rank_in_year;

--- Driver Violation Trends Based on Age and Race (Join with Subquery)
SELECT 
    td.driver_race,
    td.driver_age_group,
    td.violation,
    COUNT(*) AS violation_count,
    ROUND(100.0 * COUNT(*) / NULLIF(totals.total_stops, 0), 2) AS percent_within_group
FROM (
    SELECT 
        driver_race,
        CASE 
            WHEN driver_age < 18 THEN 'Under 18'
            WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
            WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
            WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
            ELSE '60+' 
        END AS driver_age_group,
        COUNT(*) AS total_stops
    FROM traffic_data
    WHERE driver_age IS NOT NULL AND driver_race IS NOT NULL
    GROUP BY driver_race, driver_age_group
) totals
JOIN (
    SELECT 
        driver_race,
        CASE 
            WHEN driver_age < 18 THEN 'Under 18'
            WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
            WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
            WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
            ELSE '60+' 
        END AS driver_age_group,
        violation
    FROM traffic_data
    WHERE driver_age IS NOT NULL AND driver_race IS NOT NULL AND violation IS NOT NULL
) td
ON td.driver_race = totals.driver_race AND td.driver_age_group = totals.driver_age_group
GROUP BY 
    td.driver_race, 
    td.driver_age_group, 
    td.violation,
    totals.total_stops
ORDER BY 
    td.driver_race, 
    td.driver_age_group, 
    violation_count DESC;

--- Time Period Analysis of Stops (Joining with Date Functions) , Number of Stops by Year,Month, Hour of the Day
SELECT 
    t.year,
    t.month,
    t.hour,
    COUNT(td.*) AS stop_count
FROM (
    SELECT 
        EXTRACT(YEAR FROM stop_date)::INT AS year,
        EXTRACT(MONTH FROM stop_date)::INT AS month,
        EXTRACT(HOUR FROM stop_time)::INT AS hour,
        stop_date,
        stop_time
    FROM traffic_data
    WHERE stop_date IS NOT NULL AND stop_time IS NOT NULL
) t
JOIN traffic_data AS td
  ON td.stop_date = t.stop_date
 AND td.stop_time = t.stop_time
GROUP BY t.year, t.month, t.hour
ORDER BY t.year, t.month, t.hour;

-- Alertnative for above ---
WITH time_info AS (
    SELECT 
        EXTRACT(YEAR FROM stop_date)::INT AS year,
        EXTRACT(MONTH FROM stop_date)::INT AS month,
        EXTRACT(HOUR FROM stop_time::TIME)::INT AS hour
    FROM traffic_data
    WHERE stop_date IS NOT NULL AND stop_time IS NOT NULL
)

SELECT 
    year,
    month,
    hour,
    COUNT(*) AS stop_count
FROM time_info
GROUP BY year, month, hour
ORDER BY year, month, hour;

--- Violations with High Search and Arrest Rates
SELECT 
    violation,
    ROUND(100.0 * total_arrests / NULLIF(SUM(total_arrests) OVER (), 0), 2) AS arrest_rate_percent,
	ROUND(100.0 * total_searches / NULLIF(SUM(total_searches) OVER (), 0), 2) AS search_rate_percent
FROM (
    SELECT
        violation,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN search_conducted THEN 1 ELSE 0 END) AS total_searches,
        SUM(CASE WHEN is_arrested THEN 1 ELSE 0 END) AS total_arrests
    FROM traffic_data
    WHERE violation IS NOT NULL
    GROUP BY violation
) v_stats
ORDER BY arrest_rate_percent DESC, search_rate_percent DESC;



--- To find data type of DB columns
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'public' AND table_name = 'traffic_data';

