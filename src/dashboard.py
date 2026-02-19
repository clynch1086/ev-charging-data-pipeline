import pandas as pd
import matplotlib.pyplot as plt
from db import get_engine

def show_dashboard():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM raw_data", engine)

    # Build Aggregations
    sessions_by_location = df.groupby("charging_station_location").size()

    avg_energy_by_location = (
        df.groupby("charging_station_location")["energy_consumed_kwh"].mean()
    )

    stations_by_charger_type = df["charger_type"].value_counts()

    energy_by_day_of_week = (
        df.groupby("day_of_week")["energy_consumed_kwh"].sum()
    )

    avg_cost_by_charger_type = (
        df.groupby("charger_type")["cost_usd"].mean()
    )

    # Create 5 Separate Figures
    plt.figure(figsize=(8, 5))
    plt.bar(sessions_by_location.index, sessions_by_location.values, color="skyblue")
    plt.title("Total Charging Sessions by Location")
    plt.xlabel("Station Location")
    plt.ylabel("Total Sessions")
    plt.xticks(rotation=20)

    plt.figure(figsize=(8, 5))
    plt.bar(avg_energy_by_location.index, avg_energy_by_location.values, color="orange")
    plt.title("Average Energy Consumed by Location (kWh)")
    plt.xlabel("Station Location")
    plt.ylabel("Avg Energy (kWh)")
    plt.xticks(rotation=20)

    plt.figure(figsize=(8, 5))
    plt.bar(stations_by_charger_type.index, stations_by_charger_type.values, color="green")
    plt.title("Number of Stations by Most Common Charger Type")
    plt.xlabel("Charger Type")
    plt.ylabel("Number of Stations")
    plt.xticks(rotation=45)

    plt.figure(figsize=(8, 5))
    plt.bar(energy_by_day_of_week.index, energy_by_day_of_week.values, color="purple")
    plt.title("Total Energy Consumed by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Total Energy (kWh)")
    plt.xticks(rotation=45)

    plt.figure(figsize=(8, 5))
    plt.bar(avg_cost_by_charger_type.index, avg_cost_by_charger_type.values, color="red")
    plt.title("Average Charging Cost by Charger Type (USD)")
    plt.xlabel("Charger Type")
    plt.ylabel("Avg Cost (USD)")
    plt.xticks(rotation=20)

    plt.show()