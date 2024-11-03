FROM python:3.10-slim

# Install PostgreSQL client and development packages
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Python packages with the email extra for Pydantic
RUN pip install fastapi uvicorn sqlalchemy psycopg2 pydantic[email] passlib pyjwt python-multipart

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
