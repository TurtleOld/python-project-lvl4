lint:
	poetry run flake8 task_manager

test-coverage:
	poetry run pytest --cov=task_manager

start:
	python manage.py collectstatic --noinput
	poetry run python manage.py runserver

install:
	poetry install
		
heroku:
		git push heroku main
		
github:
		git push origin main