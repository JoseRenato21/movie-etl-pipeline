"""Carrega a amostra de tests/fixtures/popular_page.json na camada Bronze.

Serve para desenvolver e testar o dbt sem precisar de um token do TMDB.
"""
import json
from pathlib import Path

from src.load import load

FIXTURE = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "popular_page.json"

if __name__ == "__main__":
    pagina = json.loads(FIXTURE.read_text(encoding="utf-8"))
    load([pagina])
