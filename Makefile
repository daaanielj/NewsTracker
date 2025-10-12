# Start everything (Docker + app)
start:
	python run.py

# Stop Docker services
stop:
	docker compose down

# Run tests
test:
	pytest -v

# Format code
format:
	black src tests

# Lint code
lint:
	ruff check src tests
