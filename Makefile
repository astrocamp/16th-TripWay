install:
	- node install
	- npm install
run poetry:
	- poetry install
	- poetry shell
run server:
	poetry run python manage.py runserver
migrations:
	poetry run python manage.py makemigrations
migrate:
	poetry run python manage.py migrate


