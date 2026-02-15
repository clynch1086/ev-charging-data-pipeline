import pandas as pd
from db import get_engine


csv_file_path = "/Users/luisagonzalez/ev_charging_project/data/raw/ev_charging_patterns.csv"
#read CSV 
df=pd.read_csv(csv_file_path)

#checking the first few lines of the data 
print(df.head)
print(f"Read CSV: {csv_file_path}, shape: {df.shape}")

#Connect to mysql
#Defined get_engine() in db.py 
engine = get_engine()

#Load the dataframe into mysql table "raw_data"
df.to_sql(name="raw_data", con=engine, if_exists='replace' ,index=False)
print(f"CSV {csv_file_path} loaded into 'raw_data' succesfully")

