import httpx
import pytest

from src.extract import extract


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_extrai_todas_as_paginas(monkeypatch):
    monkeypatch.setenv("TMDB_API_TOKEN", "token-de-teste")
    paginas = []

    def handler(request: httpx.Request) -> httpx.Response:
        paginas.append(request.url.params["page"])
        assert request.headers["Authorization"] == "Bearer token-de-teste"
        return httpx.Response(200, json={"page": int(request.url.params["page"]), "results": [{"id": 1}]})

    dados = extract(pages=3, client=_client(handler))

    assert paginas == ["1", "2", "3"]
    assert [d["page"] for d in dados] == [1, 2, 3]


def test_falha_da_api_interrompe_a_extracao(monkeypatch):
    monkeypatch.setenv("TMDB_API_TOKEN", "token-de-teste")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"status_message": "Invalid API key"})

    with pytest.raises(httpx.HTTPStatusError):
        extract(pages=2, client=_client(handler))


def test_sem_token_falha_com_mensagem_clara(monkeypatch):
    monkeypatch.delenv("TMDB_API_TOKEN", raising=False)
    monkeypatch.setattr("src.extract.load_dotenv", lambda *a, **k: None)

    with pytest.raises(RuntimeError, match="TMDB_API_TOKEN"):
        extract(pages=1)
