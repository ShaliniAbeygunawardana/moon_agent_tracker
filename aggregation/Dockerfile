FROM python:3.11-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install psycopg2


CMD ["python", "app/aggregator.py"]