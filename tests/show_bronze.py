import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

def show_bronze() -> pd.DataFrame:
    
    conn = psycopg2.connect(**config)
    

    return pd.read_sql("SELECT * FROM bronze_movies", conn)

