lint:
		poetry run flake8 task_manager task_manager/users task_manager/statuses task_manager/tasks task_manager/labels

test-coverage:
		@poetry run coverage run manage.py test

start:
		@poetry run python manage.py runserver

install:
		poetry install
		
heroku:
		git push heroku main
		
github:
		git push origin main

test:
		@poetry run coverage run --source='.' manage.py test

test-coverage-report-xml:
		@poetry run coverage xml

heroku-migrate:
		heroku run python manage.py migrate

heroku-make-migrations:
		heroku run python manage.py makemigrations

coverage:
		@poetry run coverage run manage.py test
		@poetry run coverage xml
		@poetry run coverage report