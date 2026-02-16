import pandas as pd
import matplotlib.pyplot as plt
from db import get_engine

def show_dashboard():
    #connect to mysql
    engine = get_engine()

    #Read processed station metrics 
    df=pd.read_sql("SELECT * FROM processed_station_metrics", con =engine)

    #check
    print(df.head())

    #  Dashboard 1: Total sessions per station 
    plt.figure(figsize=(8,5))
    plt.bar(df['location'], df['total_sessions'], color='skyblue')
    plt.title("Total Charging Sessions per Station")
    plt.xlabel("Station Location")
    plt.ylabel("Total Sessions")
    plt.tight_layout()
    plt.show()

    #  Dashboard 2: Average energy consumed per station 
    plt.figure(figsize=(8,5))
    plt.bar(df['location'], df['avg_energy_kwh'], color='orange')
    plt.title("Average Energy Consumed per Station (kWh)")
    plt.xlabel("Station Location")
    plt.ylabel("Avg Energy (kWh)")
    plt.tight_layout()
    plt.show()

    # Dashboard 3: Most common charger type per station
    plt.figure(figsize=(8,5))
    df_charger = df.groupby('most_common_charger_type')['station_id'].count()
    df_charger.plot(kind='bar', color='green')
    plt.title("Number of Stations by Most Common Charger Type")
    plt.xlabel("Charger Type")
    plt.ylabel("Number of Stations")
    plt.tight_layout()
    plt.show()

    # 2. Energy Demand Dashboard
   
    df_energy = pd.read_sql("SELECT * FROM processed_energy_demand;", con=engine)
    print("Energy Demand Table (first 5 rows):")
    print(df_energy.head())

    #  plot Total energy by day of week
    plt.figure(figsize=(8,5))
    df_energy.groupby("day_of_week")["total_energy_kwh"].sum().plot(kind='bar', color='purple')
    plt.title("Total Energy Consumed by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Total Energy (kWh)")
    plt.tight_layout()
    plt.show()

   
    # 3. Cost & Efficiency Dashboard

    df_cost = pd.read_sql("SELECT * FROM processed_cost_efficiency;", con=engine)
    print("Cost & Efficiency Table (first 5 rows):")
    print(df_cost.head())

    # plot Average cost per station
    plt.figure(figsize=(8,5))
    plt.bar(df_cost['charger_type'], df_cost['avg_cost_usd'], color='red')
    plt.title("Average Charging Cost per Station (USD)")
    plt.xlabel("Station ID")
    plt.ylabel("Avg Cost (USD)")
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    show_dashboard()