import pandas as pd
from db import get_engine
from pathlib import Path
from sqlalchemy import text

DATASET_NAME = "ev_charging_patterns"

def load_raw_data():
    print("Loading raw EV charging data...")

    #Get Project Root dynamically 
    project_root = Path(__file__).resolve().parent.parent
    csv_file_path = project_root / "data" / "raw" / "ev_charging_patterns.csv"

    print(f"Reading data from: {csv_file_path}")
    
    # Read CSV
    df = pd.read_csv(csv_file_path)

    # Normalize column names to be SQL-safe and consistent
    df = df.rename(columns={
        "User ID": "user_id",
        "Vehicle Model": "vehicle_model",
        "Battery Capacity (kWh)": "battery_capacity_kwh",
        "Charging Station ID": "charging_station_id",
        "Charging Station Location": "charging_station_location",
        "Charging Start Time": "charging_start_time",
        "Charging End Time": "charging_end_time",
        "Charging Duration (hours)": "charging_duration_hours",
        "Energy Consumed (kWh)": "energy_consumed_kwh",
        "Charging Rate (kW)": "charging_rate_kw",
        "Charging Cost (USD)": "cost_usd",
        "State of Charge (Start %)": "soc_start_pct",
        "State of Charge (End %)": "soc_end_pct",
        "Distance Driven (since last charge) (km)": "distance_since_last_charge_km",
        "Temperature (°C)": "temperature_c",
        "Vehicle Age (years)": "vehicle_age_years",
        "Charger Type": "charger_type",
        "User Type": "user_type",
        "Time of Day": "time_of_day",
        "Day of Week": "day_of_week",
    })
    df.columns = (
    df.columns.str.strip()
             .str.replace(" ", "_")
             .str.replace("(", "", regex=False)
             .str.replace(")", "", regex=False)
    )

    # Parse timestamps (critical for incremental logic)
    df["charging_start_time"] = pd.to_datetime(df["charging_start_time"], errors="coerce")
    df["charging_end_time"] = pd.to_datetime(df["charging_end_time"], errors="coerce")

    # Connect to MySQL
    engine = get_engine()

    # 1) Ensure metadata table exists
    create_metadata_sql = """
    CREATE TABLE IF NOT EXISTS pipeline_metadata (
      dataset_name VARCHAR(100) PRIMARY KEY,
      last_loaded_start_time DATETIME NULL,
      last_run TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """

    with engine.begin() as conn:
        conn.execute(text(create_metadata_sql))

        # 2) Read last loaded timestamp
        row = conn.execute(
            text("SELECT last_loaded_start_time FROM pipeline_metadata WHERE dataset_name = :name"),
            {"name": DATASET_NAME},
        ).fetchone()

        last_loaded = row[0] if row else None

    if last_loaded is not None:
        print(f"Last loaded charging_start_time = {last_loaded}")
        new_df = df[df["charging_start_time"] > pd.Timestamp(last_loaded)].copy()
    else:
        print("No previous load found (first run). Loading full dataset.")
        new_df = df.copy()

    # Optional: drop rows that failed datetime parsing (keeps comparisons safe)
    new_df = new_df.dropna(subset=["charging_start_time"])

    if new_df.empty:
        print("No new rows to load. Raw data is already up to date.")
        return

    # 3) Append only the new rows
    # NOTE: if raw_data doesn't exist, to_sql will create it automatically.
    new_df.to_sql(
        name="raw_data",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )

    max_loaded = new_df["charging_start_time"].max().to_pydatetime()
    print(f"Loaded {len(new_df)} new rows into 'raw_data'. New max start_time = {max_loaded}")

    # 4) Update metadata to the max timestamp loaded
    upsert_sql = """
    INSERT INTO pipeline_metadata (dataset_name, last_loaded_start_time)
    VALUES (:name, :ts)
    ON DUPLICATE KEY UPDATE
      last_loaded_start_time = GREATEST(
        COALESCE(last_loaded_start_time, '1900-01-01'),
        VALUES(last_loaded_start_time)
      );
    """

    with engine.begin() as conn:
        conn.execute(text(upsert_sql), {"name": DATASET_NAME, "ts": max_loaded})

    print("Metadata table updated successfully.")