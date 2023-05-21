init:
	python3 -m venv venv
	source venv/bin/activate && pip install --upgrade pip wheel
	if [ -f requirements.txt ]; then source venv/bin/activate && pip install -r requirements.txt; fi

test:
	source venv/bin/activate && pytest

run:
	source venv/bin/activate && uvicorn main:app --reload

migration:
	@if [ -z "$(message)" ]; then \
		echo "Please provide a migration message. Example: make migrate message='Version 1'"; \
	else \
		source venv/bin/activate && alembic revision --autogenerate -m "$(message)"; \
		alembic upgrade head; \
	fi

lint:
	source venv/bin/activate && flake8 app

format:
	source venv/bin/activate && black app

.PHONY: init test run lint format
