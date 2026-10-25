FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 10000

CMD ["sh", "-c", "gunicorn --chdir app --bind 0.0.0.0:${PORT:-10000} app:app"]
