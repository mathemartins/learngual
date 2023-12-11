#!/bin/bash
cd /app/

/opt/venv/bin/celery -A learngual worker -l INFO --concurrency 1 -P solo