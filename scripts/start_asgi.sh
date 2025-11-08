#!/bin/bash
set -e

echo "Starting Courier Core with ASGI server (Daphne) for WebSocket support..."

# Build CSS and collect static files
npm run build:css
python manage.py collectstatic --noinput

# Start Daphne ASGI server
daphne -b 0.0.0.0 -p 5000 courier.asgi:application
