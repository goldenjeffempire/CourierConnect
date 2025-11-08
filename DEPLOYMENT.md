# Deployment Guide - Courier Core

This guide covers deploying the Courier Core application to production using Render (recommended) and alternative deployment options.

##  Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Git
- Render account (for Render deployment)

## Deployment Options

### Option 1: Render (Recommended)

Render provides managed PostgreSQL, Redis, and easy Python deployments.

#### Step 1: Prepare Your Repository

1. Ensure all code is committed to Git
2. Push to GitHub/GitLab
3. Verify `render.yaml` is in the repository root

#### Step 2: Connect to Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New" → "Blueprint"
3. Connect your repository
4. Render will automatically detect `render.yaml`

#### Step 3: Configure Environment Variables

Add these environment variables in the Render dashboard:

```bash
# Django Settings
SECRET_KEY=<generate-a-secure-random-key>
DJANGO_SETTINGS_MODULE=courier.settings.prod
ALLOWED_HOSTS=.onrender.com,yourdomain.com

# Database (Automatically set by Render if using managed Postgres)
DATABASE_URL=<automatically-provided-by-render>

# Redis (Automatically set if using managed Redis)
REDIS_URL=<automatically-provided-by-render>

# Payment Providers (Demo keys shown - replace with real ones)
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
PAYSTACK_SECRET_KEY=sk_test_YOUR_KEY_HERE

# Map Services
MAPBOX_TOKEN=pk.YOUR_MAPBOX_TOKEN
GOOGLE_MAPS_API_KEY=YOUR_GOOGLE_MAPS_KEY

# Monitoring
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# Notifications
TWILIO_ACCOUNT_SID=YOUR_TWILIO_SID
TWILIO_AUTH_TOKEN=YOUR_TWILIO_TOKEN
TWILIO_PHONE_NUMBER=+1234567890

# Email
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=YOUR_SENDGRID_API_KEY
```

#### Step 4: Deploy

1. Click "Apply" in Render dashboard
2. Render will:
   - Create PostgreSQL database
   - Create Redis instance
   - Build and deploy your app
   - Run migrations automatically

#### Step 5: Post-Deployment

```bash
# Create superuser (via Render shell)
python manage.py createsuperuser

# Seed demo data
python scripts/seed_demo_data.py

# Collect static files (should be automatic)
python manage.py collectstatic --noinput
```

### Option 2: Docker Deployment

#### Build and Run with Docker

```bash
# Build the image
docker build -t courier-core:latest .

# Run with docker-compose
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Seed demo data
docker-compose exec web python scripts/seed_demo_data.py
```

#### Production Docker Deployment

```bash
# Use production settings
docker-compose -f docker-compose.prod.yml up -d
```

### Option 3: Manual VPS Deployment

#### Prerequisites on Server

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install python3.11 python3.11-venv postgresql postgresql-contrib redis-server nginx

# Create application user
sudo useradd -m -s /bin/bash courier
sudo su - courier
```

#### Clone and Setup

```bash
# Clone repository
git clone https://github.com/yourorg/courier-core.git
cd courier-core

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

#### Configure Database

```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE courier_production;
CREATE USER courier_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE courier_production TO courier_user;
\q
```

#### Environment Configuration

```bash
# Create .env file
cp .env.example .env
nano .env  # Edit with your production values
```

#### Run Migrations and Collect Static

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### Setup Gunicorn Service

Create `/etc/systemd/system/courier.service`:

```ini
[Unit]
Description=Courier Core Gunicorn Service
After=network.target

[Service]
User=courier
Group=courier
WorkingDirectory=/home/courier/courier-core
Environment="PATH=/home/courier/courier-core/venv/bin"
ExecStart=/home/courier/courier-core/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/courier/courier-core/courier.sock \
    --timeout 120 \
    courier.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable courier
sudo systemctl start courier
sudo systemctl status courier
```

#### Configure Nginx

Create `/etc/nginx/sites-available/courier`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/courier/courier-core/staticfiles/;
    }

    location /media/ {
        alias /home/courier/courier-core/media/;
    }

    location / {
        proxy_pass http://unix:/home/courier/courier-core/courier.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/courier /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | Yes | - |
| `DEBUG` | Debug mode | No | False |
| `ALLOWED_HOSTS` | Comma-separated hosts | Yes | - |
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `REDIS_URL` | Redis connection string | Yes | - |
| `STRIPE_PUBLISHABLE_KEY` | Stripe public key | No | - |
| `STRIPE_SECRET_KEY` | Stripe secret key | No | - |
| `MAPBOX_TOKEN` | Mapbox API token | No | - |
| `SENTRY_DSN` | Sentry error tracking | No | - |

## Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY` (at least 50 random characters)
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Enable HTTPS/SSL
- [ ] Set up database backups
- [ ] Configure firewall rules
- [ ] Use environment variables for secrets
- [ ] Enable CSRF protection
- [ ] Set up monitoring (Sentry)
- [ ] Configure rate limiting
- [ ] Regular security updates

## Monitoring and Maintenance

### Health Checks

```bash
# Check application status
curl https://yourdomain.com/admin/

# Check database connection
python manage.py dbshell

# Check Redis connection
redis-cli -u $REDIS_URL ping
```

### Logs

```bash
# Application logs (systemd)
sudo journalctl -u courier -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Database Backups

```bash
# Backup database
pg_dump courier_production > backup_$(date +%Y%m%d).sql

# Restore database
psql courier_production < backup_20240101.sql
```

## Troubleshooting

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput --clear
sudo systemctl restart courier
```

### Database Connection Issues

```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Test connection
python manage.py dbshell
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R courier:courier /home/courier/courier-core
chmod -R 755 /home/courier/courier-core
```

## Scaling Considerations

### Horizontal Scaling

- Use load balancer (Nginx, HAProxy)
- Session storage in Redis
- Shared media storage (S3, CloudFlare R2)
- Database read replicas

### Performance Optimization

- Enable Redis caching
- Use CDN for static files
- Database query optimization
- Celery for background tasks
- Connection pooling

## Support

For deployment issues:
- Check logs first
- Review error messages in Sentry
- Consult Django deployment documentation
- Contact support@globalswift.com
