# Courier Core - Enterprise Package Delivery Platform

**Last Updated**: November 8, 2025

## Overview
A production-ready courier management web application built with Django, featuring real-time tracking, payment integration, and role-based dashboards for customers, couriers, and administrators.

## Current State
✅ **Fully Imported and Working**
- All Python dependencies installed
- Database migrations completed
- Demo data seeded with test accounts
- Server running on port 5000
- Static files collected

## Tech Stack
- **Backend**: Django 4.2.9 + Django REST Framework
- **Database**: SQLite (development), PostgreSQL-ready for production
- **Real-time**: Django Channels + Redis (WebSocket support)
- **Payment**: Stripe integration with demo keys
- **Queue**: Celery + Redis for background tasks
- **Frontend**: Django Templates + Tailwind CSS + HTMX + Alpine.js
- **Server**: Gunicorn

## Project Structure
```
courier-core/
├── apps/
│   ├── users/          # Authentication & user management
│   ├── parcels/        # Shipment management
│   ├── tracking/       # Real-time package tracking
│   ├── payments/       # Stripe payment processing
│   ├── notifications/  # Email/SMS notifications
│   └── admin_panel/    # Admin dashboard
├── courier/
│   ├── settings/       # Environment-based settings (base, dev, prod)
│   ├── wsgi.py         # WSGI application
│   └── asgi.py         # ASGI application for WebSockets
├── templates/          # HTML templates
├── static/            # Static files
├── staticfiles/       # Collected static files
└── scripts/           # Utility scripts (seed data, etc.)
```

## Test Accounts
After seeding demo data:
- **Admin**: username=`admin`, password=`admin123`
- **Customer**: username=`customer1`, password=`password123`
- **Courier**: username=`courier1`, password=`password123`

## Features
- Multi-role system (Customer, Courier, Admin) with RBAC
- Real-time package tracking with GPS location updates
- Stripe payment integration (using demo keys)
- Email and SMS notifications via Celery
- Proof of delivery with OTP confirmation
- Interactive maps (Mapbox integration)
- Mobile-responsive design

## Environment Configuration
Environment variables are stored in `.env` file with demo/placeholder values:
- Django SECRET_KEY
- Stripe API keys (demo)
- Mapbox token (demo)
- Twilio credentials (demo)
- Email configuration (console backend for dev)

## Workflow Configuration
- **Name**: web
- **Command**: `gunicorn courier.wsgi:application --bind 0.0.0.0:5000 --workers 2 --timeout 120`
- **Port**: 5000
- **Type**: Web application with webview output

## Common Commands
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed demo data
python scripts/seed_demo_data.py

# Collect static files
python manage.py collectstatic --noinput

# Run tests
pytest

# Format code
black .
isort .
```

## Recent Changes
- **2025-11-08**: Project imported to Replit environment
  - Installed all Python dependencies from requirements.txt
  - Created .env file from .env.example
  - Ran database migrations successfully
  - Seeded demo data (16 users, 20 parcels, 66 tracking events)
  - Configured Gunicorn workflow on port 5000
  - Application running and accessible

## Notes
- WebSocket features require running with Daphne/ASGI server instead of Gunicorn
- All API keys are demo/placeholder values for development
- For real-time tracking features, consider switching to Daphne server
- Static files served via WhiteNoise middleware
- Database uses SQLite for development (PostgreSQL recommended for production)

## Next Steps & Enhancements
Potential areas for future development:
- Switch to Daphne server for WebSocket support
- Set up Redis service for real-time features and caching
- Add real API keys for Stripe, Twilio, Mapbox (when deploying)
- Configure Celery worker for background tasks
- Set up PostgreSQL database for production
- Implement additional courier features
- Enhance tracking visualization
- Add more comprehensive tests
