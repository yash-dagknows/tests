# Makefile for DagKnows Test Suite
# Provides convenient commands for running tests

.PHONY: help install test test-unit test-integration test-e2e test-coverage clean setup-env start-services stop-services logs

# Default target
.DEFAULT_GOAL := help

# Environment
SHELL := /bin/bash
PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker-compose -f docker-compose-test.yml
PYTEST := pytest

# Directories
TEST_DIR := .
RESULTS_DIR := results
LOGS_DIR := logs

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)DagKnows Test Suite$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install test dependencies
	@echo "$(GREEN)Installing test dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Dependencies installed!$(NC)"

setup-env: ## Setup test environment (copy .env files, create directories)
	@echo "$(GREEN)Setting up test environment...$(NC)"
	@test -f .env.test || (cp .env.test.example .env.test && echo ".env.test created from example")
	@mkdir -p $(RESULTS_DIR) $(LOGS_DIR)
	@echo "$(GREEN)Test environment ready!$(NC)"

start-services: setup-env ## Start test services (docker-compose)
	@echo "$(GREEN)Starting test services...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)Waiting for services to be healthy...$(NC)"
	@./utils/wait-for-services.sh
	@echo "$(GREEN)All services are ready!$(NC)"

stop-services: ## Stop test services
	@echo "$(RED)Stopping test services...$(NC)"
	$(DOCKER_COMPOSE) down

clean-services: ## Stop and remove test services including volumes
	@echo "$(RED)Cleaning up test services and data...$(NC)"
	$(DOCKER_COMPOSE) down -v
	@echo "$(RED)Cleanup complete!$(NC)"

logs: ## Show logs from test services
	$(DOCKER_COMPOSE) logs -f

logs-service: ## Show logs for specific service (usage: make logs-service SERVICE=taskservice)
	@test -n "$(SERVICE)" || (echo "$(RED)ERROR: SERVICE not specified$(NC)" && exit 1)
	$(DOCKER_COMPOSE) logs -f $(SERVICE)

test: setup-env ## Run all tests
	@echo "$(GREEN)Running all tests...$(NC)"
	$(PYTEST) -v --color=yes

test-unit: ## Run unit tests only
	@echo "$(GREEN)Running unit tests...$(NC)"
	$(PYTEST) unit/ -v --color=yes -m unit

test-integration: start-services ## Run integration tests (requires services)
	@echo "$(GREEN)Running integration tests...$(NC)"
	$(PYTEST) integration/ -v --color=yes -m integration
	@$(MAKE) stop-services

test-e2e: start-services ## Run end-to-end tests (requires services)
	@echo "$(GREEN)Running end-to-end tests...$(NC)"
	$(PYTEST) e2e/ -v --color=yes -m e2e
	@$(MAKE) stop-services

test-smoke: start-services ## Run smoke tests for quick validation
	@echo "$(GREEN)Running smoke tests...$(NC)"
	$(PYTEST) -v --color=yes -m smoke
	@$(MAKE) stop-services

test-fast: ## Run only fast unit tests
	@echo "$(GREEN)Running fast tests...$(NC)"
	$(PYTEST) unit/ -v --color=yes -m "unit and not slow"

test-coverage: setup-env ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(PYTEST) -v --color=yes \
		--cov=../taskservice/src \
		--cov=../req_router/src \
		--cov-report=html:$(RESULTS_DIR)/htmlcov \
		--cov-report=term-missing \
		--cov-report=xml:$(RESULTS_DIR)/coverage.xml
	@echo "$(GREEN)Coverage report generated in $(RESULTS_DIR)/htmlcov/$(NC)"

test-docker: ## Run tests inside Docker container
	@echo "$(GREEN)Running tests in Docker...$(NC)"
	$(DOCKER_COMPOSE) up --abort-on-container-exit test-runner
	@$(MAKE) stop-services

test-parallel: setup-env ## Run tests in parallel (faster)
	@echo "$(GREEN)Running tests in parallel...$(NC)"
	$(PYTEST) -v --color=yes -n auto

test-watch: ## Run tests in watch mode (re-run on file changes)
	@echo "$(GREEN)Running tests in watch mode...$(NC)"
	$(PYTEST) -v --color=yes -f

test-specific: ## Run specific test file (usage: make test-specific FILE=test_file.py)
	@test -n "$(FILE)" || (echo "$(RED)ERROR: FILE not specified$(NC)" && exit 1)
	@echo "$(GREEN)Running tests in $(FILE)...$(NC)"
	$(PYTEST) $(FILE) -v --color=yes

test-by-marker: ## Run tests with specific marker (usage: make test-by-marker MARKER=slow)
	@test -n "$(MARKER)" || (echo "$(RED)ERROR: MARKER not specified$(NC)" && exit 1)
	@echo "$(GREEN)Running tests with marker: $(MARKER)...$(NC)"
	$(PYTEST) -v --color=yes -m $(MARKER)

test-failed: ## Re-run only failed tests from last run
	@echo "$(GREEN)Re-running failed tests...$(NC)"
	$(PYTEST) -v --color=yes --lf

test-debug: ## Run tests with debug output
	@echo "$(GREEN)Running tests with debug output...$(NC)"
	$(PYTEST) -v --color=yes -s --log-cli-level=DEBUG

test-pdb: ## Run tests with PDB debugger on failure
	@echo "$(GREEN)Running tests with PDB debugger...$(NC)"
	$(PYTEST) -v --color=yes --pdb

clean: ## Clean test artifacts and cache
	@echo "$(RED)Cleaning test artifacts...$(NC)"
	@rm -rf .pytest_cache
	@rm -rf $(RESULTS_DIR)/*
	@rm -rf $(LOGS_DIR)/*
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(RED)Cleanup complete!$(NC)"

clean-all: clean clean-services ## Clean everything including Docker volumes

lint: ## Run linting checks
	@echo "$(GREEN)Running linting checks...$(NC)"
	@black --check .
	@isort --check-only .
	@flake8 .

format: ## Format code with black and isort
	@echo "$(GREEN)Formatting code...$(NC)"
	@black .
	@isort .

report: ## Generate HTML test report
	@echo "$(GREEN)Generating test report...$(NC)"
	$(PYTEST) -v --color=yes --html=$(RESULTS_DIR)/report.html --self-contained-html
	@echo "$(GREEN)Report generated: $(RESULTS_DIR)/report.html$(NC)"

ci-test: setup-env ## Run tests in CI mode (with JUnit XML output)
	@echo "$(GREEN)Running tests in CI mode...$(NC)"
	$(PYTEST) -v --color=yes \
		--junitxml=$(RESULTS_DIR)/junit.xml \
		--cov=../taskservice/src \
		--cov=../req_router/src \
		--cov-report=xml:$(RESULTS_DIR)/coverage.xml \
		--cov-report=html:$(RESULTS_DIR)/htmlcov \
		--html=$(RESULTS_DIR)/report.html \
		--self-contained-html

shell: ## Open a shell in the test environment
	@echo "$(GREEN)Opening test shell...$(NC)"
	$(DOCKER_COMPOSE) run --rm test-runner /bin/bash

check-services: ## Check health of test services
	@echo "$(GREEN)Checking service health...$(NC)"
	@$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "$(GREEN)Testing service endpoints...$(NC)"
	@curl -s http://localhost:9300/_cluster/health | python3 -m json.tool || echo "$(RED)Elasticsearch not ready$(NC)"
	@curl -s http://localhost:2235/api/v1/tasks/status || echo "$(RED)TaskService not ready$(NC)"
	@curl -s http://localhost:8888/health || echo "$(RED)Req-Router not ready$(NC)"

init: install setup-env ## Initialize everything (first-time setup)
	@echo "$(GREEN)Initialization complete!$(NC)"
	@echo "$(BLUE)Run 'make test' to run tests$(NC)"
	@echo "$(BLUE)Run 'make help' to see all available commands$(NC)"

.PHONY: test-tenant test-task test-auth
test-tenant: ## Run tenant-related tests only
	$(PYTEST) -v --color=yes -m tenant

test-task: ## Run task-related tests only
	$(PYTEST) -v --color=yes -m task

test-auth: ## Run authentication tests only
	$(PYTEST) -v --color=yes -m auth

