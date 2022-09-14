help:
	@echo "help"
	@echo "make help - this message"
	@echo "make setup - install dependencies"
	@echo "make dev - run development server at localhost:5000"
	@echo "make prod - run production server at localhost:8080"

setup:
	python3 -m pip install poetry
	python3 -m poetry install

dev:
	python3 -m poetry run flask run

prod:
	python3 -m poetry run waitress-serve --port 8080 --call 'app:create_app' 