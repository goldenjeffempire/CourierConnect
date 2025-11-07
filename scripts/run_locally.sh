#!/bin/bash

echo "Starting Courier Core locally..."

if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Creating superuser (if needed)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@couriercore.com', 'admin123', role='admin')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting development server..."
python manage.py runserver 0.0.0.0:5000
