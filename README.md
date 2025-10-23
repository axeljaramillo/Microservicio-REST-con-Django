# Courses API (Django + DRF + drf-yasg)

A simple microservice that models an online courses platform (users, courses, lessons, enrollments, comments) with Django REST Framework. Includes automatic API docs via Swagger and Redoc.

## Features
- CRUD endpoints for users, courses, lessons, enrollments, and comments
- Relational models with Django ORM
- Filtering, searching, ordering
- Swagger UI at `/swagger/` and Redoc at `/redoc/`
- Dockerized with PostgreSQL

## Quickstart (Docker)

```bash
# From this folder
docker compose build
# This will run DB migrations and start the dev server
docker compose up
```

Then open:
- App: http://localhost:8500/
- API root (router): http://localhost:8500/api/
- Swagger: http://localhost:8500/swagger/
- Redoc: http://localhost:8500/redoc/

### Common management commands
```bash
# Create admin user
docker compose exec web python manage.py createsuperuser

# Generate migrations (if you change models)
docker compose exec web python manage.py makemigrations courses_api

# Apply migrations
docker compose exec web python manage.py migrate

# List routes via DRF
docker compose exec web python manage.py show_urls || true
```

## Endpoints (high-level)
- `POST /api/users/` create user (password is write-only). `GET /api/users/` list users.
- `GET/POST/PUT/PATCH/DELETE /api/courses/` manage courses. Instructor defaults to authenticated user on create.
- `GET/POST/... /api/lessons/` lessons per course with `filter[course]=<id>` support.
- `POST /api/enrollments/` enroll current user (if `user` omitted) into a course.
- `POST /api/comments/` create a comment for a course (user defaults to current user).

## Configuration notes
- Database is configured for the compose `db` service (PostgreSQL 15).
- Allowed hosts include `localhost`, `0.0.0.0`, and `web`.
- Token auth is enabled; you can create tokens via DRF authtoken if desired.

## Development without Docker
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=...  # or update settings.py
python manage.py migrate
python manage.py runserver
```

## Screenshots
Add screenshots of Swagger, container running, and example requests as required by your submission.

---

Made for educational purposes.
