# Makefile

# Define the command to run tools inside the uv environment
RUN = uv run

.PHONY: install test

install:
	@echo "Installing dependencies..."
	uv sync --all-extras --dev

test:
	@echo "Running tests..."
	$(RUN) python -m unittest discover tests
