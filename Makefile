install:
	- node install
	- npm install
run poetry:
	- poetry install
	- poetry shell
runserver:
	poetry run python manage.py runserver
migrations:
	poetry run python manage.py makemigrations
migrate:
	poetry run python manage.py migrate


