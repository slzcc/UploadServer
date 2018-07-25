FROM python:3
COPY . /UploadInterface
WORKDIR /UploadInterface
RUN pip install --upgrade pip && pip install -r package.txt

ENV UPLOAD_FILE_PATH = "/storage/" \
    NGINX_MIRROR_URL = "http://localhost/" \
    NGINX_MIRROR_STORAGE_PATH = "firmware/resume" \
    REMOVE_SOURCE_FILE_SETUP = False

EXPOSE 8878 8877
CMD uwsgi --socket 0.0.0.0:8877 \
      --chdir /UploadInterface/ \
      --env DJANGO_SETTINGS_MODULE=UploadInterface.settings \
      --module "django.core.handlers.wsgi:WSGIHandler()" \
      --processes 4 \
      --threads 2 \
      --workers 5 \
      --http 0.0.0.0:8878 \
      --uid root --gid root \
      --master --vacuum \
      --thunder-lock \
      --enable-threads \
      --harakiri 30 \
      --post-buffering 4096 \
      --file "/UploadInterface/UploadInterface/wsgi.py"
