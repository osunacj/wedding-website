# Dockerfile
FROM python:3.12

RUN apt-get update && apt-get install nginx --yes

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY deploy/prod-requirements.txt prod-requirements.txt
RUN pip install --no-cache-dir -r prod-requirements.txt

COPY deploy/nginx.conf /etc/nginx/sites-enabled/default

# Mounts the application code to the image
COPY . app
WORKDIR /app

EXPOSE 8080

# runs the production server
CMD ["/bin/bash", "-c", "python manage.py collectstatic --noinput; python manage.py migrate; python manage.py createsuperuser --noinput; /usr/sbin/nginx -g 'daemon off;' & gunicorn bigday.wsgi --bind 0.0.0.0:8000"]
