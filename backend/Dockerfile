FROM python:3.12-slim

WORKDIR /app

# System deps needed by common Python packages (psycopg/asyncpg build tools,
# and later phases like unstructured[pdf] need libmagic/poppler — added when
# that phase lands so this image doesn't carry weight it doesn't need yet).
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
