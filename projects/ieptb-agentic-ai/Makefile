install:
	python -m pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check .

evaluate:
	PYTHONPATH=. python evaluation/run.py

run:
	uvicorn src.api.main:app --reload

security:
	pytest -q tests/test_security.py tests/test_api.py
