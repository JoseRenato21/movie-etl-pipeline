"""Carga: grava as páginas extraídas na camada Bronze (JSONB cru)."""
import json

import psycopg2.extras
from loguru import logger

from src.db import connect

CREATE_BRONZE = """
CREATE TABLE IF NOT EXISTS bronze_movies (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    extracted_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_bronze_movies_extracted_at
    ON bronze_movies (extracted_at);
"""


def load(data: list[dict]) -> int:
    """Insere cada página como uma linha em bronze_movies. Devolve quantas linhas gravou."""
    rows = [(json.dumps(page),) for page in data]
    # O "with" fecha a transação sozinho: confirma se tudo der certo e desfaz em caso de erro.
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_BRONZE)
            psycopg2.extras.execute_values(
                cur, "INSERT INTO bronze_movies (data) VALUES %s", rows
            )
    logger.info("{} páginas gravadas em bronze_movies", len(rows))
    return len(rows)
