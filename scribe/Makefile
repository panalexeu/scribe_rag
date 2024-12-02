all:
	fastapi dev src/api/app.py

chroma:
	chroma run --port 8001

test_unit:
	pytest tests/unit

test_integr:
	pytest tests/integr

test_docs:
	pytest tests/documents

test_e2e:
	pytest tests/e2e

test:
	pytest -p no:warnings

test_ver:
	pytest -vs -p no:warnings --tb=long