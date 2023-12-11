#!/bin/bash

APP_PORT=${PORT:-8000}
cd /app/
/opt/venv/bin/daphne learngual.asgi:application --port $PORT --bind 0.0.0.0 -v2 ## && /opt/venv/bin/celery -A learngual worker -l INFO --concurrency 1 -P solo && /opt/venv/bin/celery -A learngual beat -l INFO