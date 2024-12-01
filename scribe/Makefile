all:
	fastapi dev src/api/app.py

chroma:
	chroma run --port 8001

chroma_fake:
	chroma run --path ./chroma_fake --port 8001

rm_chroma_fake:
	rm -rf ./chroma_fake

test:
	pytest

test_unit:
	pytest tests/unit

test_e2e:
	pytest tests/e2e

test_integr:
	pytest tests/integr -v

test_async:
	pytest tests/documents