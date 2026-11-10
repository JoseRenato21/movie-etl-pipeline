"""Conexão com o PostgreSQL a partir das variáveis de ambiente."""
import os

import psycopg2
from dotenv import load_dotenv


def connect():
    """Abre uma conexão usando DB_HOST, DB_PORT, DB_NAME, DB_USER e DB_PASSWORD."""
    load_dotenv()
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "filmes"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )
