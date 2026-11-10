"""Teste de integração: precisa de um PostgreSQL acessível pelas variáveis DB_*.

Sem banco disponível, o teste é ignorado em vez de falhar.
"""
import json
from pathlib import Path

import psycopg2
import pytest

from src.db import connect
from src.load import load

FIXTURE = Path(__file__).parent / "fixtures" / "popular_page.json"


@pytest.fixture
def conn():
    try:
        c = connect()
    except psycopg2.OperationalError:
        pytest.skip("PostgreSQL indisponível")
    with c.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS bronze_movies")
    c.commit()
    yield c
    c.close()


def test_load_grava_uma_linha_por_pagina(conn):
    pagina = json.loads(FIXTURE.read_text(encoding="utf-8"))

    gravadas = load([pagina, pagina])

    assert gravadas == 2
    with conn.cursor() as cur:
        cur.execute("SELECT count(*), min(jsonb_array_length(data -> 'results')) FROM bronze_movies")
        linhas, filmes_por_pagina = cur.fetchone()
    assert linhas == 2
    assert filmes_por_pagina == len(pagina["results"])
