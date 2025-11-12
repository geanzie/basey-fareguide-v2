#!/bin/sh

# Exit on error
set -e

echo "========================================="
echo "Starting Basey Fare Guide Backend"
echo "========================================="

echo "Running collectstatic..."
python manage.py collectstatic --noinput --clear || echo "Collectstatic failed, continuing..."

echo "Starting gunicorn on port ${PORT:-8000}..."
exec gunicorn bfg.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
