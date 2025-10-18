.PHONY: help install install-dev fmt lint typecheck test test-integration test-cov run run-prod docker-build docker-up docker-down clean

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies"
	@echo "  make install-dev      - Install dev dependencies"
	@echo "  make fmt              - Format code"
	@echo "  make lint             - Run linters"
	@echo "  make typecheck        - Run type checker"
	@echo "  make test             - Run all tests"
	@echo "  make test-integration - Run integration tests"
	@echo "  make test-cov         - Run tests with coverage"
	@echo "  make run              - Run development server"
	@echo "  make run-prod         - Run production server"
	@echo "  make docker-build     - Build Docker images"
	@echo "  make docker-up        - Start Docker services"
	@echo "  make docker-down      - Stop Docker services"
	@echo "  make clean            - Clean cache files"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

fmt:
	@echo "Running isort..."
	isort app tests
	@echo "Running black..."
	black app tests
	@echo "Running ruff fix..."
	ruff check --fix app tests || true

lint:
	@echo "Running ruff..."
	ruff check app tests
	@echo "Running isort check..."
	isort --check-only app tests
	@echo "Running black check..."
	black --check app tests

typecheck:
	@echo "Running mypy..."
	mypy app

test:
	pytest tests/ -v

test-integration:
	pytest tests/integration/ -v

test-cov:
	pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-prod:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-up-prod:
	docker-compose --profile production up -d app-prod

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f app

clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	@echo "Cache cleaned!"

