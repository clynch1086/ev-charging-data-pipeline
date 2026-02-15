import sqlalchemy

from sqlalchemy import create_engine 

def get_engine():
    engine = create_engine(
        "mysql+pymysql://root:Azucar2020!@localhost:3306/ev_charging_db"
    )
    return engine 

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