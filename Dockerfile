# Start with a Python image.
FROM python:3.10
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
RUN mkdir /code/static
WORKDIR /code


RUN apt-get update && apt-get install -y libgdal-dev

RUN apt-get install poppler-utils
RUN pip install GDAL==3.2.2.1
RUN pip install numpy psycopg2-binary

RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

RUN python manage.py collectstatic --noinput
