FROM python:3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/

RUN python3 -m pip install -r /app/requirements.txt