FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install fastapi uvicorn sqlalchemy psycopg2 pydantic[email] passlib pyjwt python-multipart

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
