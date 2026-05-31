from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
import json
import os

def load(data: list[dict])-> None:
    load_dotenv()
    
    with psycopg2.connect( # with assume a responsabilidade de se fechar sozinho, até quando existir um erro    
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        ) as conn:  #se der erro o conn fecha automaticamente
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS bronze_movies (
                        id SERIAL PRIMARY KEY,
                        data JSONB NOT NULL,
                        extracted_at TIMESTAMP DEFAULT NOW()
                    );
                    CREATE INDEX IF NOT EXISTS idx_bronze_movies_id 
                        ON bronze_movies ((data->>'id'));
                    CREATE INDEX IF NOT EXISTS idx_bronze_movies_extracted_at 
                        ON bronze_movies (extracted_at);
                    """)
                conn.commit()
                
                rows = []
                for movie in data:
                    stringJson = json.dumps(movie)
                    tupla = (stringJson,) #vira tupla
                    rows.append(tupla)
                psycopg2.extras.execute_values(cur, "INSERT INTO bronze_movies (data) VALUES %s", rows)   
                conn.commit()