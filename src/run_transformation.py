import pymysql
from db import get_engine
import pandas as pd

# Get raw connection
engine = get_engine()
conn = engine.raw_connection()
cursor = conn.cursor()

with open("sql/transform_data.sql", "r") as f:
    sql_query = f.read()


for statement in sql_query.split(";"):
    if statement.strip(): #skip empty lines in transform_data.sql
        cursor.execute(statement) 

conn.commit()
cursor.close()
conn.close()

print("SQL script successfully executed")

df=pd.read_sql("SELECT * FROM processed_data LIMIT 10;", con=engine)
print(df)