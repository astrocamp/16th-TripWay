install:
	- npm install
	- poetry install
runserverserver:
	poetry run python manage.py runserver
migrations:
	poetry run python manage.py makemigrations
migrate:
	poetry run python manage.py migrate