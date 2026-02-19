-- Table 1: Station Metrics 

DROP TABLE IF EXISTS processed_station_metrics;

CREATE TABLE processed_station_metrics AS
SELECT
    charging_station_id AS station_id,
    charging_station_location AS location,
    COUNT(*) AS total_sessions,
    AVG(energy_consumed_kwh) AS avg_energy_kwh,
    AVG(charging_duration_hours) AS avg_duration_hr,
    AVG(cost_usd) AS avg_cost_usd,
    AVG(temperature_c) AS avg_temp_c,
    (
        SELECT charger_type
        FROM raw_data r2
        WHERE r2.charging_station_id = r1.charging_station_id
          AND r2.charging_station_location = r1.charging_station_location
        GROUP BY charger_type
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) AS most_common_charger_type
FROM raw_data r1
GROUP BY charging_station_id, charging_station_location;

-- Table 2: Energy Demand Analysis
DROP TABLE IF EXISTS processed_energy_demand;

CREATE TABLE processed_energy_demand AS
SELECT
    charging_station_location AS location,
    day_of_week AS day_of_week,
    time_of_day AS time_of_day,
    SUM(energy_consumed_kwh) AS total_energy_kwh,
    COUNT(*) AS total_sessions
FROM raw_data
GROUP BY
    charging_station_location,
    day_of_week,
    time_of_day;

-- Table 3: Cost and Efficiency
DROP TABLE IF EXISTS processed_cost_efficiency;

CREATE TABLE processed_cost_efficiency AS
SELECT
    charger_type AS charger_type,
    AVG(charging_duration_hours) AS avg_duration_hr,
    AVG(cost_usd) AS avg_cost_usd,
    AVG(energy_consumed_kwh) AS avg_energy_kwh
FROM raw_data
GROUP BY charger_type;


