FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The admin's static assets; the app itself is a JSON API.
RUN SECRET_KEY=build MONGO_HOST=mongodb://localhost:27017/build \
    python manage.py collectstatic --noinput || true

EXPOSE 8000
# Long timeout: a speaking answer waits on transcription plus analysis.
CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 180"]
