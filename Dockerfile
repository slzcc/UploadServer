FROM python:3
COPY . /UploadInterface
WORKDIR /UploadInterface
RUN pip install --upgrade pip && pip install -r package.txt

ENV UPLOAD_FILE_PATH = "/storage/" \
    NGINX_MIRROR_URL = "http://localhost/" \
    NGINX_MIRROR_STORAGE_PATH = "firmware/resume"

EXPOSE 8878
CMD python3 manage.py runserver 0.0.0.0:8878
