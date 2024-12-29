FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install -U pip

WORKDIR /Code
COPY ./requirements.txt /Code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /Code/