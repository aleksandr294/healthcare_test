# Healthcare_test

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

Django admin http://localhost/admin/

Healthcare_app swagger http://localhost/api/schema/swagger-ui/

Healthcare_analytics swagger http://localhost/analytics/docs

## Requirements
- Docker version 29.1.3

## Setup
   ```
   git clone git@github.com:aleksandr294/healthcare_test.git
   cd healthcare_test/
   docker build -f infrastructure/docker/Dockerfile.base -t healthcare-test-base:latest . && docker compose -f infrastructure/docker/docker-compose.yml -p healthcare-test-system up --build
   ```

# System Architecture

The system is built using a microservices architecture and is divided into clearly defined areas of responsibility.

## General Overview

- Operational logic (CRUD operations, business rules, workflows) is implemented in Django
- Background and scheduled tasks are handled by Celery
- Analytics and aggregated data are provided by a separate FastAPI service
- All services communicate via HTTP using JWT-based authentication
