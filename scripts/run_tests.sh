#!/bin/bash
set -e

echo "Running Higgsfield API tests..."

# Format check
echo "=== Checking code format ==="
isort --check-only app tests
black --check app tests

# Linting
echo "=== Running linters ==="
ruff check app tests

# Type checking
echo "=== Running type checker ==="
mypy app

# Tests
echo "=== Running tests ==="
pytest tests/ -v --cov=app --cov-report=term-missing

echo "✅ All checks passed!"

