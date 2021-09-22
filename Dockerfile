# syntax=docker/dockerfile:1
FROM python:3.9.5
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
