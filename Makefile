.PHONY: help install install-dev test lint format clean build upload

help:
	@echo "OrganiserPro Development Commands"
	@echo "================================="
	@echo "install      - Install the package"
	@echo "install-dev  - Install development dependencies"
	@echo "test         - Run tests"
	@echo "lint         - Run linting checks"
	@echo "format       - Format code with black"
	@echo "clean        - Clean build artifacts"
	@echo "build        - Build distribution packages"
	@echo "upload       - Upload to PyPI (maintainers only)"

install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.in
	pip install -e .

test:
	python -m pytest tests/ -v

lint:
	flake8 OrganiserPro/
	mypy OrganiserPro/

format:
	black OrganiserPro/
	black tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

upload: build
	python -m twine upload dist/*

desktop-install:
	./install_desktop.sh

desktop-uninstall:
	rm -f ~/.local/share/applications/organiserpro.desktop
	rm -f ~/.local/share/icons/organiserpro.png
