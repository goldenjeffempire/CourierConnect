# Courier Core - Enterprise Package Delivery Platform

A complete courier web product built with Django, featuring real-time tracking, payment integration, and role-based dashboards.

## Features

- **Multi-Role System**: Customer, Courier, and Admin roles with RBAC
- **Real-Time Tracking**: Django Channels + Redis for WebSocket updates (with polling fallback)
- **Payment Integration**: Stripe integration with demo keys and Paystack placeholder
- **Interactive Maps**: Mapbox integration for live GPS tracking
- **Notifications**: Email + SMS alerts via Celery background tasks
- **Proof of Delivery**: OTP confirmation and photo/signature upload
- **Responsive UI**: Mobile-first design with Tailwind CSS + HTMX + Alpine.js
- **Production Ready**: Docker, CI/CD, comprehensive tests, deployment configs

## Tech Stack

- **Backend**: Django 4.2.9 + Django REST Framework
- **Real-time**: Django Channels 4.0 + Redis
- **Database**: PostgreSQL (SQLite for local dev)
- **Cache/Queue**: Redis + Celery
- **Frontend**: Django Templates + Tailwind CSS + HTMX + Alpine.js
- **Containerization**: Docker + docker-compose
- **CI/CD**: GitHub Actions
- **Deployment**: Render (recommended)

## Quick Start

### Local Development

1. **Clone and setup**:
```bash
git clone <repository-url>
cd courier-core
cp .env.example .env
```

2. **Run with Docker** (recommended):
```bash
docker-compose up --build
```

3. **Or run locally**:
```bash
chmod +x scripts/run_locally.sh
./scripts/run_locally.sh
```

4. **Seed demo data**:
```bash
python scripts/seed_demo_data.py
```

5. **Access the application**:
- Application: http://localhost:5000
- Admin: http://localhost:5000/admin

### Test Accounts

- **Admin**: `admin` / `admin123`
- **Customer**: `customer1` / `password123`
- **Courier**: `courier1` / `password123`

## Project Structure

```
courier-core/
├── .github/workflows/     # CI/CD configurations
├── apps/                  # Django apps
│   ├── users/            # Authentication & user management
│   ├── parcels/          # Shipment management
│   ├── tracking/         # Real-time tracking
│   ├── payments/         # Payment processing
│   ├── notifications/    # Email/SMS notifications
│   └── admin_panel/      # Admin dashboard
├── courier/              # Django project settings
│   └── settings/         # Environment-based settings
├── templates/            # HTML templates
├── static/              # Static files (CSS, JS, images)
├── tests/               # Test suite
├── scripts/             # Utility scripts
├── docs/                # Documentation
├── docker/              # Docker configurations
├── Dockerfile           # Production Docker image
├── docker-compose.yml   # Local development setup
├── render.yaml          # Render deployment config
└── requirements.txt     # Python dependencies
```

## Environment Variables

See `.env.example` for all configuration options. Key variables:

```env
SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0

# Payment Providers (Demo Keys)
STRIPE_PUBLISHABLE_KEY=pk_test_DEMO
STRIPE_SECRET_KEY=sk_test_DEMO
PAYSTACK_SECRET_KEY=sk_test_PAYSTACK_DEMO

# Maps & Notifications
MAPBOX_TOKEN=pk.mapbox_demo_token
TWILIO_ACCOUNT_SID=ACDEMO
TWILIO_AUTH_TOKEN=DEMO
```

## Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=apps --cov-report=html

# Specific app
pytest apps/parcels/tests/
```

## Deployment

### Render (Recommended)

1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy using the provided `render.yaml` configuration

See [docs/deployment.md](docs/deployment.md) for detailed instructions.

### GitHub Pages + Render (Optional)

For static marketing pages on GitHub Pages with API on Render:
1. Export static pages using django-distill
2. Deploy static files to GitHub Pages
3. Configure CORS for API access

**Important**: GitHub Pages only hosts static sites. Dynamic features (tracking, payments, WebSockets) must be deployed to Render or similar platforms.

## Core Workflows

### Create Shipment
1. Customer logs in
2. Creates shipment with pickup/delivery addresses
3. Gets instant price quote based on weight, distance, service level
4. Completes payment via Stripe
5. Receives tracking number

### Track Package
1. Enter tracking number on homepage
2. View real-time location on interactive map
3. See delivery history and status updates
4. Receive notifications at each milestone

### Courier Workflow
1. Courier logs in to mobile-friendly dashboard
2. Accepts assigned deliveries
3. Updates GPS location in real-time
4. Marks packages as picked up/delivered
5. Collects OTP or proof of delivery

## API Integration (Demo Keys)

All integrations use placeholder demo keys for development:

- **Stripe**: Demo keys for payment processing
- **Paystack**: Placeholder for alternative payment
- **Mapbox**: Demo token for maps
- **Twilio**: Demo credentials for SMS
- **Sentry**: Optional error tracking

Replace with real keys in production.

## Security Features

- CSRF protection on all forms
- Rate limiting on authentication endpoints
- Input validation and sanitization
- Upload size limits for proof-of-delivery
- TLS enforcement in production
- Session security (secure cookies in prod)
- Data minimization for GPS logs

## Performance

- Pagination on all listing endpoints
- Database indexing on frequently queried fields
- Redis caching for session data
- Static file compression with WhiteNoise
- Asynchronous task processing with Celery

## Scaling Recommendations

When to split into microservices:
- Tracking service (>10,000 active shipments)
- Payments service (>1,000 transactions/day)
- Notifications service (>100,000 notifications/day)

See [docs/PRODUCTION.md](docs/PRODUCTION.md) for production checklist.

## Development

### Code Quality

```bash
# Format code
black .
isort .

# Lint
flake8 .
ruff check .
```

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file

## Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Documentation: [docs/](docs/)

---

**Note**: This is a demo application using placeholder API keys. Replace all demo keys with real credentials before deploying to production.
