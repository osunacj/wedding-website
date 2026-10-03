# Dockerfile
FROM python:3.12-slim

# tzdata isn't in the slim image; zoneinfo needs it for WEDDING_TIMEZONE.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends nginx tzdata \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY deploy/nginx.conf /etc/nginx/sites-enabled/default

# Copies the application code into the image, already owned by www-data (a
# separate chown -R would store a second copy of every file in a new layer).
COPY --chown=www-data:www-data . app
WORKDIR /app

# Run as the unprivileged user nginx's own package already created, instead of root.
# nginx's default pid path (/run/nginx.pid) isn't writable by a non-root user, so
# point it at /tmp instead.
RUN sed -i 's#pid /run/nginx.pid;#pid /tmp/nginx.pid;#' /etc/nginx/nginx.conf \
    && chown -R www-data:www-data /var/log/nginx /var/lib/nginx
USER www-data

EXPOSE 8080

# runs the production server
CMD ["/bin/bash", "-c", "python manage.py collectstatic --noinput; python manage.py migrate; python manage.py createsuperuser --noinput; /usr/sbin/nginx -g 'daemon off;' & gunicorn bigday.wsgi --bind 127.0.0.1:8000"]
