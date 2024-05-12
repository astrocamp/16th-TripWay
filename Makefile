install:
	- node install
	- npm install
run poetry:
	- poetry install
	- poetry shell
run server:
	python manage.py runserver
migrations:
	python manage.py makemigrations
migrate:
	python manage.py migrate


