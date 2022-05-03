lint:
	poetry run flake8 task_manager users

test-coverage:
	python manage.py test --keepdb

start:
	poetry run python manage.py runserver

install:
	poetry install
		
heroku:
		git push heroku main
		
github:
		git push origin main