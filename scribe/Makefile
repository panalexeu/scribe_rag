all:
	fastapi dev src/api/app.py

chroma:
	chroma run --port 8001

test_unit:
	pytest tests/unit -v

test_integr:
	pytest tests/integr -v

test_docs:
	pytest tests/documents -v

test_e2e:
	./e2e_script.sh

test:
	make test_unit
	make test_integr
	make test_docs
	make test_e2e