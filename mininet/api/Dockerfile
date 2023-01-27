FROM python:3.8-slim-buster

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

# CMD ["python3", "/app/api/app.py"]
CMD ["tail", "-f", "/dev/null"]