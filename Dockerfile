FROM python:3
COPY . /UploadInterface
WORKDIR /UploadInterface
RUN pip install -r package.txt

EXPOSE 8878
CMD python3 mamane.py runserver 0.0.0.0:8878
