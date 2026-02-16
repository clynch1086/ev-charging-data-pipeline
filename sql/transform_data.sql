-- Table 1: Station Metrics 

DROP TABLE IF EXISTS processed_station_metrics;

CREATE TABLE processed_station_metrics AS
SELECT
    `Charging Station ID` AS station_id,
    `Charging Station Location` AS location,
    COUNT(*) AS total_sessions,
    AVG(`Energy Consumed (kWh)`) AS avg_energy_kwh,
    AVG(`Charging Duration (hours)`) AS avg_duration_hr,
    AVG(`Charging Cost (USD)`) AS avg_cost_usd,
    AVG(`Temperature (°C)`) AS avg_temp_c,
    (
        SELECT `Charger Type`
        FROM raw_data r2
        WHERE r2.`Charging Station ID` = r1.`Charging Station ID`
          AND r2.`Charging Station Location` = r1.`Charging Station Location`
        GROUP BY `Charger Type`
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) AS most_common_charger_type
FROM raw_data r1
GROUP BY `Charging Station ID`, `Charging Station Location`;

-- Table 2: Energy Demand Analysis 
DROP TABLE IF EXISTS processed_energy_demand;

CREATE TABLE processed_energy_demand AS
SELECT
    `Charging Station Location` AS location,
    `Day of Week` AS day_of_week,
    `Time of Day` AS time_of_day,
    SUM(`Energy Consumed (kWh)`) AS total_energy_kwh,
    COUNT(*) AS total_sessions
FROM raw_data
GROUP BY 
    `Charging Station Location`,
    `Day of Week`,
    `Time of Day`;

-- Table 3: Cost and Efficiency
DROP TABLE IF EXISTS processed_cost_efficiency;

CREATE TABLE processed_cost_efficiency AS
SELECT
    `Charger Type` AS charger_type,
    AVG(`Charging Duration (hours)`) AS avg_duration_hr,
    AVG(`Charging Cost (USD)`) AS avg_cost_usd,
    AVG(`Energy Consumed (kWh)`) AS avg_energy_kwh
FROM raw_data
GROUP BY `Charger Type`;


