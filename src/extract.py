"""Extração: lê os filmes populares da API do TMDB, uma página por vez."""
import os

import httpx
from dotenv import load_dotenv
from loguru import logger

BASE_URL = "https://api.themoviedb.org/3/movie/popular"
PAGES = 9


def extract(pages: int = PAGES, client: httpx.Client | None = None) -> list[dict]:
    """Devolve a resposta JSON crua de cada página, sem alterar nada.

    A camada Bronze guarda o dado exatamente como chegou. Por isso nenhuma
    transformação acontece aqui. Se uma página falhar, a execução inteira falha:
    carregar páginas parciais deixaria o Bronze incompleto sem avisar.
    """
    load_dotenv()
    token = os.getenv("TMDB_API_TOKEN")
    if not token:
        raise RuntimeError("Defina TMDB_API_TOKEN no .env (veja .env.example).")

    headers = {"Authorization": f"Bearer {token}"}
    own_client = client is None
    client = client or httpx.Client(timeout=30)

    data: list[dict] = []
    try:
        for page in range(1, pages + 1):
            response = client.get(BASE_URL, params={"page": page}, headers=headers)
            response.raise_for_status()
            data.append(response.json())
            logger.info("página {} extraída ({} filmes)", page, len(data[-1].get("results", [])))
    except httpx.HTTPStatusError as e:
        logger.error("a API respondeu {} para {}", e.response.status_code, e.request.url)
        raise
    except httpx.RequestError as e:
        logger.error("falha de rede ao chamar a API: {}", e)
        raise
    finally:
        if own_client:
            client.close()
    return data
