# Makefile for AI Agent Project Setup
PYTHON = python3.11
VENV = .venv
ACTIVATE = . $(VENV)/bin/activate

# Folder structure based on your initial request
DIRS = \
	config \
	data/docs \
	src/agents \
	src/utils/ \
	src/workflows \
	tests/utils

.PHONY: help setup clean test

help:
	@echo "AI Agent Project Management"
	@echo "Commands:"
	@echo "  make setup    - Create folder structure and setup environment"
	@echo "  make test     - Run environment validation tests"
	@echo "  make clean    - Remove virtual environment and build artifacts"

setup: create-dirs venv install-torch install-deps test

create-dirs:
	@echo "Creating folder structure..."
	@mkdir -p $(DIRS)
	@touch config/settings.py src/main.py

venv:
	@echo "Creating Python 3.11 virtual environment..."
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created in $(VENV)"

install-torch: venv
	@echo "Installing PyTorch 2.5.0 with CUDA 12.4 support..."
	@$(ACTIVATE) && pip install \
		torch==2.5.0+cu124 \
		torchvision==0.20.0+cu124 \
		torchaudio==2.5.0+cu124 \
		--extra-index-url https://download.pytorch.org/whl/cu124

install-deps: venv
	@echo "Installing project dependencies..."
	@$(ACTIVATE) && pip install -r requirements.txt

test:
	@echo "Running environment validation tests..."
	@python tests/utils/gpu_check.py
	@python tests/utils/test_versions.py
	@python tests/utils/test_install.py
	@echo "All tests passed!"

clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV)
	@rm -rf __pycache__ */__pycache__ */*/__pycache__
	@echo "Clean complete"