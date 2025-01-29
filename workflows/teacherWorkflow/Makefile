
SHELL := /bin/bash
# Makefile for AI Agent Project Setup
PYTHON_REQUIRED = 3.11
PYTHON = python3.11
VENV = .venv

ACTIVATE = source $(VENV)/bin/activate

.PHONY: help setup clean test check-python re

help:
	@echo "AI Agent Project Management"
	@echo "Commands:"
	@echo "  make setup    - Create folder structure and setup environment"
	@echo "  make test     - Run environment validation tests"
	@echo "  make clean    - Remove virtual environment and build artifacts"
	@echo "  make re       - Full clean and rebuild"

setup: check-python venv update-pip install-torch install-deps test

check-python:
	@echo "Checking Python version..."
	@if ! which $(PYTHON) > /dev/null; then \
		echo "ERROR: Python $(PYTHON_REQUIRED) not found!"; \
		echo "Recommendation: Install Python $(PYTHON_REQUIRED) using pyenv for better version management"; \
		echo "1. Install pyenv: https://github.com/pyenv/pyenv#installation"; \
		echo "2. Install Python $(PYTHON_REQUIRED): pyenv install 3.11.6"; \
		echo "3. Set as default: pyenv global 3.11.6"; \
		exit 1; \
	fi
	@echo "Python $(PYTHON_REQUIRED) verified ($$(python3.11 --version))"

venv: check-python
	@echo "Creating Python $(PYTHON_REQUIRED) virtual environment..."
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created in $(VENV)"

update-pip: venv
	@echo "Upgrading pip to latest version..."
	@$(ACTIVATE); pip install --upgrade pip

install-torch: venv
	@echo "Installing PyTorch 2.5.0 with CUDA 12.4 support..."
	@$(ACTIVATE); pip install \
		torch==2.5.0+cu124 \
		torchvision==0.20.0+cu124 \
		torchaudio==2.5.0+cu124 \
		--extra-index-url https://download.pytorch.org/whl/cu124

install-deps: venv
	@echo "Installing project dependencies..."
	@$(ACTIVATE); pip install -r requirements.txt

test:
	@echo "Running environment validation tests..."
	@$(ACTIVATE); python tests/utils/gpu_check.py && \
	 				python tests/utils/test_versions.py && \
	 				python tests/utils/test_install.py
	@echo "All tests passed!"

clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV)
	@rm -rf __pycache__ */__pycache__ */*/__pycache__
	@find . -name '*.pyc' -delete
	@echo "Clean complete"

re: clean setup