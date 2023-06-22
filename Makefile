init:
	python3 -m venv venv
	source venv/bin/activate && pip install --upgrade pip wheel
	if [ -f requirements.txt ]; then source venv/bin/activate && pip install -r requirements.txt; fi
	source venv/bin/activate && pip install python-dotenv

test-dev:
	source venv/bin/activate && export $(shell cat .env.dev | xargs) && pytest

test-prod:
	source venv/bin/activate && export $(shell cat .env.prod | xargs) && pytest

run-dev:
	source venv/bin/activate && export $(shell cat .env.dev | xargs) && uvicorn main:app --reload

run-prod:
	source venv/bin/activate && export $(shell cat .env.prod | xargs) && uvicorn main:app --reload

migration-dev:
	@if [ -z "$(message)" ]; then \
		echo "Please provide a migration message. Example: make migrate message='Version 1'"; \
	else \
		source venv/bin/activate && export $(shell cat .env.dev | xargs) && \
		python alembic_config.py && \
		alembic revision --autogenerate -m "$(message)"; \
		alembic upgrade head; \
	fi

migration-prod:
	@if [ -z "$(message)" ]; then \
		echo "Please provide a migration message. Example: make migrate message='Version 1'"; \
	else \
		source venv/bin/activate && export $(shell cat .env.prod | xargs) && \
		python alembic_config.py && \
		alembic revision --autogenerate -m "$(message)"; \
		alembic upgrade head; \
	fi

lint-dev:
	source venv/bin/activate && export $(shell cat .env.dev | xargs) && flake8 app

lint-prod:
	source venv/bin/activate && export $(shell cat .env.prod | xargs) && flake8 app

format-dev:
	source venv/bin/activate && export $(shell cat .env.dev | xargs) && black app

format-prod:
	source venv/bin/activate && export $(shell cat .env.prod | xargs) && black app

.PHONY: init test-dev test-prod run-dev run-prod migration-dev migration-prod lint-dev lint-prod format-dev format-prod
