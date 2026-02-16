import pandas as pd
from db import get_engine

def load_raw_data():
    csv_file_path = "/Users/luisagonzalez/ev_charging_project/data/raw/ev_charging_patterns.csv"
    
    # Read CSV
    df = pd.read_csv(csv_file_path)
    print(df.head())
    print(f"Read CSV: {csv_file_path}, shape: {df.shape}")

    # Connect to MySQL
    engine = get_engine()

    # Load the dataframe into MySQL table "raw_data"
    df.to_sql(name="raw_data", con=engine, if_exists='replace', index=False)
    print(f"CSV {csv_file_path} loaded into 'raw_data' successfully")
