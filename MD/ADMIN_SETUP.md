# Admin Panel Setup Guide

## Admin Panel App Structure

The admin panel code has been modularized into a dedicated `admin_panel` app for better organization:

```
admin_panel/
├── __init__.py
├── apps.py
├── admin_site.py      # Custom secure admin site
├── middleware.py      # Admin security middleware
├── registry.py        # Model registration
├── models.py
├── views.py
└── tests.py
```

## Features

### 1. Modular Admin Code
- All admin-related code is in the `admin_panel` app
- Clean separation of concerns
- Easy to maintain and extend

### 2. Consolidated CSS
- All admin CSS in one file: `static/admin/css/admin.css`
- Comprehensive styling for all admin components
- Responsive design
- Custom color scheme (Parsa Journal branding)

### 3. Consolidated JavaScript
- All admin JS in one file: `static/admin/js/admin.js`
- Form validation
- Auto-hide messages
- Enhanced UX features
- Security warnings

### 4. Security Features
- IP whitelist support
- Rate limiting (5 attempts per 15 minutes)
- Access logging
- Custom admin URL
- Enhanced permission checks

## Setup Instructions

### 1. Create .env File
```bash
cp .env.example .env
# Edit .env and update configuration
```

### 2. Setup Database
```bash
# Option 1: Use setup script
./setup_database.sh

# Option 2: Manual setup
sudo -u postgres psql
CREATE DATABASE parsajournal_db;
CREATE USER postgres WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE parsajournal_db TO postgres;
\q
```

### 3. Run Migrations
```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Start Server
```bash
python manage.py runserver
```

## Database Management

Use the `manage_db.sh` script for database operations:

```bash
# Start PostgreSQL
./manage_db.sh start

# Stop PostgreSQL
./manage_db.sh stop

# Check status
./manage_db.sh status

# Run migrations
./manage_db.sh migrate

# Create superuser
./manage_db.sh createsuperuser

# Open database shell
./manage_db.sh shell

# Backup database
./manage_db.sh backup

# Restore database
./manage_db.sh restore backup_file.sql
```

## Admin Panel Configuration

### Custom Admin URL
Change the admin URL in `.env`:
```bash
ADMIN_URL=your-custom-url
```

### IP Whitelist
Restrict admin access to specific IPs in `.env`:
```bash
ADMIN_IP_WHITELIST=127.0.0.1,::1,your-ip-address
```

### Security Settings
All security settings are in `.env`:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (False in production)
- `SESSION_COOKIE_SECURE`: Secure cookies (True in production)
- `SECURE_SSL_REDIRECT`: SSL redirect (True in production)

## Admin Panel Styling

The admin panel uses a consolidated CSS file with:
- Custom color scheme (dark header with gold accent)
- Responsive design
- Enhanced forms and buttons
- Custom login page
- Security warnings
- Message styling
- Table styling
- Pagination styling

## Admin Panel JavaScript

The admin panel JavaScript includes:
- Form validation
- Auto-hide messages
- Delete confirmation
- Loading indicators
- Character counters
- Enhanced checkboxes
- Search highlighting
- Auto-save (optional)

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Check database credentials in .env
```

### Migration Errors
```bash
# Reset migrations (CAUTION: This will delete data)
python manage.py migrate --fake-initial

# Or create fresh migrations
python manage.py makemigrations
python manage.py migrate
```

### Admin Panel Not Loading
```bash
# Check admin_panel app is in INSTALLED_APPS
# Check admin_panel.middleware.AdminSecurityMiddleware is in MIDDLEWARE
# Check admin_panel.admin_site.admin_site is used in urls.py
```

## Security Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False` in production
- [ ] Change `ADMIN_URL` to custom value
- [ ] Set `ADMIN_IP_WHITELIST` if needed
- [ ] Set strong database password
- [ ] Enable SSL in production
- [ ] Set `SESSION_COOKIE_SECURE=True` in production
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up regular backups
- [ ] Monitor admin access logs

## Support

For issues or questions, refer to:
- `SECURITY.md` - Security configuration
- `DOCKER.md` - Docker setup
- `SETUP.md` - General setup
- `README.md` - Project overview

