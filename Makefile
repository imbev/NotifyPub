help:
	@echo "help"
	@echo "make help - this message"
	@echo "make setup - install dependencies"
	@echo "make test - run tests"
	@echo "make dev - run development server at localhost:5000"
	@echo "make prod - run production server at localhost:8080"

setup:
	python3 -m pip install poetry
	python3 -m poetry install

dev:
	python3 -m poetry run flask --debug --app 'app.app:create_app' run 

prod:
	python3 -m poetry run waitress-serve --port 8080 --call 'app.app:create_app' 