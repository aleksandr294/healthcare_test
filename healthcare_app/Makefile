.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: collectstatic
collectstatic:
	python manage.py collectstatic

.PHONY: run_app
run_app:
	gunicorn healthcare.wsgi:application -c gunicorn.conf.py

.PHONY: run_celery
run_celery_worker:
	celery -A celery_app worker --loglevel=info

.PHONY: run_celery_beat
run_celery_beat:
	celery -A celery_app beat --loglevel=info