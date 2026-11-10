DBT = uv run dbt
DBT_ARGS = --project-dir dbt --profiles-dir dbt

.PHONY: up down ingest sample dbt-seed dbt-run dbt-test pipeline test clean

up:            ## sobe o PostgreSQL em Docker
	docker compose up -d --wait

down:          ## derruba o PostgreSQL (os dados ficam no volume)
	docker compose down

ingest:        ## API do TMDB -> Bronze
	uv run python -m src.pipeline

sample:        ## carrega a amostra local no Bronze (não precisa de token)
	uv run python -m src.sample

dbt-seed:      ## carrega a tabela de gêneros
	$(DBT) seed $(DBT_ARGS)

dbt-run:       ## Bronze -> Silver -> Gold
	$(DBT) seed $(DBT_ARGS)
	$(DBT) run $(DBT_ARGS)

dbt-test:      ## testes de qualidade dos dados
	$(DBT) test $(DBT_ARGS)

pipeline: ingest dbt-run dbt-test   ## fluxo completo

test:          ## testes de unidade do código Python
	uv run pytest

clean:
	rm -rf dbt/target dbt/logs .pytest_cache
