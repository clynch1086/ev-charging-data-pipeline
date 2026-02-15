DROP TABLE IF EXISTS processed_data;

CREATE TABLE processed_data AS
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