ENV_LOCAL_COMPOSE_FILE = -f "docker-compose.local.yml"

.PHONY: up_local_environment
up_local_environment:
	docker compose $(ENV_LOCAL_COMPOSE_FILE) -p healthcare-test-local up --build

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