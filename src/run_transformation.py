from db import get_engine
import pandas as pd

def run_transformation():
    engine = get_engine()
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # Load SQL from file
    with open("sql/transform_data.sql", "r") as f:
        sql_query = f.read()

    # Execute each statement
    for statement in sql_query.split(";"):
        if statement.strip():  # skip empty lines
            cursor.execute(statement)

    conn.commit()
    cursor.close()
    conn.close()

    print("SQL script successfully executed")

    # Optional: show first 10 rows of one of the processed tables
    df = pd.read_sql("SELECT * FROM processed_station_metrics LIMIT 10;", con=engine)
    print(df)