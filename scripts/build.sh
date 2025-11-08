#!/bin/bash
set -e

echo "Building Courier Core for production..."

# Build Tailwind CSS
echo "Building Tailwind CSS..."
npm run build:css

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete!"
