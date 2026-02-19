import os
from dotenv import load_dotenv
from sqlalchemy import create_engine 

load_dotenv()

def get_engine():
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "ev_charging_db")

    connection_string = (
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    return create_engine(connection_string)

#checking to see if connection to database is succesful 
if __name__ == "__main__":
    engine = get_engine()
    try:
        # Try connecting
        connection = engine.connect()
        print("Connection to database successful!")
        connection.close()
    except Exception as e:
        print("Error connecting to database:", e)