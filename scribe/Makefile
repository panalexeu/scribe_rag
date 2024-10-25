APP_PATH=./src/api/app.py

all:
	poetry run fastapi dev $(APP_PATH)

dev:
	poetry run fastapi dev $(APP_PATH)

prod:
	poetry run fastapi run $(APP_PATH)

test:
	pytest