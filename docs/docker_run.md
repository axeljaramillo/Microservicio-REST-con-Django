# How to build, run and inspect the Dockerized project

This file shows the exact commands to build the images, run the service, follow logs, and access the API/Swagger UI.

Run from the `django_docker` directory (where `docker-compose.yaml` and `Dockerfile` live):

```bash
# 1) Build and start containers in background
docker compose up -d --build

# 2) Watch the web container logs (shows migrations, startup, and any errors)
docker compose logs -f web

# 3) Check status of containers
docker compose ps

# 4) Tail database logs (optional)
docker compose logs -f db

# 5) Open the app in your browser
# Django runserver default host:port (as configured) is:
# http://localhost:8500
# Swagger UI (drf-yasg) endpoints commonly available at:
#  - http://localhost:8500/swagger/ (Swagger UI)
#  - http://localhost:8500/redoc/   (ReDoc)
#  - http://localhost:8500/swagger.json
#  - http://localhost:8500/swagger.yaml

# 6) Example: GET the API root
curl -i http://localhost:8500/api/

# 7) Example: View a course detail (replace <id>)
curl -i http://localhost:8500/api/courses/1/detail/

# 8) Run one-off manage.py commands inside web container
docker compose exec web python manage.py showmigrations

# 9) Stop and remove containers
docker compose down

# 10) Remove volumes (data) if you want a clean DB state
docker compose down -v
```

Notes:
- The container entrypoint waits for the Postgres service to become ready, runs `makemigrations`/`migrate`, then starts Django.
- Database credentials are provided in `docker-compose.yaml` under `POSTGRES_*`. For production, don't store secrets in source control; use environment files or a secret manager.
- If the web container cannot bind to port 8500, check if some local process already uses that port (macOS):

```bash
lsof -i :8500
```

If something is using the port, either stop that process or change the host mapping in `docker-compose.yaml`.
