#!/bin/sh
set -e

# Simple DB wait using psycopg2. Relies on psycopg2-binary being installed in the image.
# Environment variables used (fall back to defaults):
#  POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, POSTGRES_PORT

DB_NAME=${POSTGRES_DB:-mydatabase}
DB_USER=${POSTGRES_USER:-user}
DB_PASS=${POSTGRES_PASSWORD:-password}
DB_HOST=${DB_HOST:-db}
DB_PORT=${POSTGRES_PORT:-5432}

echo "Waiting for database ${DB_HOST}:${DB_PORT} ..."
python - <<PY
import os, time, sys
import psycopg2
from psycopg2 import OperationalError

db_name=os.environ.get('POSTGRES_DB','%s')
db_user=os.environ.get('POSTGRES_USER','%s')
db_pass=os.environ.get('POSTGRES_PASSWORD','%s')
db_host=os.environ.get('DB_HOST','%s')
db_port=int(os.environ.get('POSTGRES_PORT',%s))

for i in range(60):
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
        conn.close()
        print('Database is available')
        sys.exit(0)
    except OperationalError:
        print('Database not ready, sleeping 1s... (%d/60)' % (i+1))
        time.sleep(1)
print('Timed out waiting for the database', file=sys.stderr)
sys.exit(1)
PY

# Run migrations non-interactively
echo "Running migrations..."
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

# Collect static (optional for dev; harmless)
# python manage.py collectstatic --noinput || true

# Exec the CMD from the Dockerfile / compose
exec "$@"
