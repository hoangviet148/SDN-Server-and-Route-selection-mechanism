FROM python:3.8-slim-buster

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]