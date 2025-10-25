format:
	@echo "Formatting code..."
	@uv run black .

run:
	@echo "Running Wiki Agent..."
	@uv run python main.py