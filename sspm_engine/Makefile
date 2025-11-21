.PHONY: install test lint clean run-api docker-build

install:
	pip install -e .

test:
	pytest tests/

lint:
	# Just a placeholder for actual linting commands
	@echo "Running linter..."
	# pylint sspm_engine/

clean:
	rm -rf build/ dist/ *.egg-info
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +

run-api:
	uvicorn sspm_engine.api.server:app --reload

run-cli-scan:
	python -m sspm_engine.cli.sspmctl scan all

docker-build:
	docker build -t sspm-engine .

docker-run:
	docker-compose up
