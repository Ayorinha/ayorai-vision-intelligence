install:
	python -m pip install -e ".[dev]"
lint:
	ruff check .
test:
	pytest -q
security:
	pytest -q tests/test_security.py tests/test_governance.py tests/test_mcp.py
evaluate:
	PYTHONPATH=. python evaluation/run.py
compile:
	python -m compileall -q src evaluation
run:
	uvicorn src.api.main:app --reload
mcp:
	python src/mcp_server.py
