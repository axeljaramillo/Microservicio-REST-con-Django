FROM python:3.11-slim
WORKDIR /app
COPY ./ /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
# Add entrypoint script that waits for DB, runs migrations and then execs the CMD
COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python","manage.py","runserver","0.0.0.0:8500"]
