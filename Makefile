init:
	python3 -m venv venv
	source venv/bin/activate && pip install --upgrade pip wheel
	if [ -f requirements.txt ]; then source venv/bin/activate && pip install -r requirements.txt; fi

test:
	source venv/bin/activate && pytest

run:
	source venv/bin/activate && python app/main.py

lint:
	source venv/bin/activate && flake8 app

format:
	source venv/bin/activate && black app

.PHONY: init test run lint format
