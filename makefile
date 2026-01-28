# Makefile

.PHONY: help check format

help:
	@echo "Available commands:"
	@echo "  make check   - Run ruff linting"
	@echo "  make format  - Run ruff formatting"
	@echo "  make         - Show this help"

check:
	uv run ruff check . --fix

format:
	uv run ruff format .