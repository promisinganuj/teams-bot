# Makefile for Teams AddBot development
.PHONY: help install dev test lint format clean docker-build docker-run deploy-local

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  dev          - Run in development mode"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  clean        - Clean up temporary files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run with Docker Compose"
	@echo "  deploy-local - Deploy to local Docker environment"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	pip install pytest pytest-asyncio black flake8 pytest-cov

# Development server
dev:
	@echo "Starting development server..."
	python app.py

# Run tests
test:
	@echo "Running tests..."
	python -m pytest tests/ -v

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage..."
	python -m pytest tests/ --cov=. --cov-report=html --cov-report=term

# Lint code
lint:
	@echo "Running linter..."
	flake8 *.py tests/ --max-line-length=88 --ignore=E203,W503

# Format code
format:
	@echo "Formatting code..."
	black *.py tests/ --line-length=88

# Clean temporary files
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage .pytest_cache/ 2>/dev/null || true

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker build -f Dockerfile.dev -t teams-addbot:dev .

docker-run:
	@echo "Starting with Docker Compose..."
	docker-compose up --build

deploy-local:
	@echo "Deploying to local Docker environment..."
	docker-compose up --build -d

# Setup development environment
setup: install
	@echo "Setting up development environment..."
	cp .env.template .env || true
	@echo "Please edit .env file with your configuration"
