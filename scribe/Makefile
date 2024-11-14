all:
	fastapi dev src/api/app.py

test:
	pytest

test_unit:
	pytest tests/unit

test_e2e:
	pytest tests/e2e

test_integr:
	pytest tests/integr -v

test_async:
	pytest tests/async