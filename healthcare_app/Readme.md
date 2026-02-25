# Healthcare_app

## Description
Default users
 - Admin
   - login - admin@mail.com
   - password - admin
 - Caregiver
   - login - caregiver@mail.com
   - password - caregiver
 - Patient
   - login - patient@mail.com
   - password - patient

URL django admin http://127.0.0.1:8000/admin

URL swagger http://127.0.0.1:8000/api/schema/swagger-ui/

The result of Celery task execution in the Task Results tab

The execution commands are stored in the Makefile

## Requirements

- Python 3.12
- Poetry
- Docker version 29.1.3

## Setup

1. **Clone repository:**

   ```
   git clone git@github.com:aleksandr294/healthcare_test.git
   cd healthcare_test/healthcare_app
   ```
   
2. **Install Poetry and django_celery_beat**

   ```
   pip install poetry django_celery_beat
   ```
   
3. **Install requirements**
   ```
   poetry install
   ```

4. **Set .env file**
   ```
    POSTGRES_URL=postgresql://user:user@127.0.0.1:15000/healthcare_db
    RABBITMQ_URL=amqp://user:password@127.0.0.1:5672
    SECRET_KEY=secret
   ```

5. Up local environment
   ```
   cd healthcare_test/infrastructure/docker/
   docker compose -f "docker-compose.local.yml" -p healthcare_test-local up --build
   ```
6. Run Migrate
   ```
   make migrate
   ```
7. Run app
   ```
   python manage.py runserver
   ```

## Linters and Tests

Install pre-commit
```
   pre-commit install
```

Run linters

```
   pre-commit run --all-files
```