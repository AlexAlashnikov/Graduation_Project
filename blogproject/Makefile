FORMAT_FOLDER?=.

format:
	python -m isort ${FORMAT_FOLDER}
	python -m black ${FORMAT_FOLDER}
	python -m flake8 ${FORMAT_FOLDER}

freeze:pip
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

pip:
	pip install $(pack)

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations && python manage.py migrate

superuser:
	python manage.py createsuperuser