"""Executa a etapa de ingestão: API do TMDB para a camada Bronze.

As camadas Silver e Gold são construídas pelo dbt (veja a pasta dbt/).
"""
from loguru import logger

from src.extract import extract
from src.load import load


def main() -> None:
    data = extract()
    load(data)
    logger.info("ingestão concluída. Rode `make dbt-run` para gerar Silver e Gold.")


if __name__ == "__main__":
    main()
