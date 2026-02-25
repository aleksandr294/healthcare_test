# Healthcare_analytics

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

URL swagger http://127.0.0.1:8000/docs/

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
   cd healthcare_test/healthcare_analytics
   ```
   
2. **Install Poetry and django_celery_beat**

   ```
   pip install poetry
   ```
   
3. **Install requirements**
   ```
   poetry install
   ```

4. **Set .env file**
   ```
    POSTGRES_URL=postgresql+asyncpg://user:user@127.0.0.1:15000/healthcare_db
    SECRET_KEY=secret
   ```

5. Up local environment
   ```
   cd healthcare_test/infrastructure/docker/
   docker compose -f "docker-compose.local.yml" -p healthcare_test-local up --build
   ```
   
6. Run Migrate
    Run migrations in healthcare_app

7. Run app
   ```
    uvicorn main:app --port 8000
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