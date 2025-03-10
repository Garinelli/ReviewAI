FROM python:3.10

WORKDIR /app

COPY prod_requirements.txt .

RUN pip install --no-cache-dir -r prod_requirements.txt

COPY src /app/src
COPY .env /app
COPY start.sh /app