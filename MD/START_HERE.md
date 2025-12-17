# 🚀 Start Here - Parsa Journal Setup

## Quick Setup Guide

### Step 1: Install Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Create .env File
```bash
# The .env file should already exist, but if not:
cp .env.example .env

# Edit .env and update:
# - SECRET_KEY (generate a new one)
# - DB_PASSWORD (set your database password)
# - Other settings as needed
```

### Step 3: Start PostgreSQL
```bash
# Check if PostgreSQL is installed and running
sudo systemctl status postgresql

# If not running, start it:
sudo systemctl start postgresql

# Enable PostgreSQL to start on boot:
sudo systemctl enable postgresql
```

### Step 4: Setup Database
```bash
# Option 1: Use setup script (recommended)
./setup_database.sh

# Option 2: Manual setup
sudo -u postgres psql
```

Then in PostgreSQL shell:
```sql
CREATE DATABASE parsajournal_db;
CREATE USER postgres WITH PASSWORD 'your-password';
ALTER DATABASE parsajournal_db OWNER TO postgres;
GRANT ALL PRIVILEGES ON DATABASE parsajournal_db TO postgres;
\q
```

### Step 5: Run Migrations
```bash
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 8: Start Server
```bash
python manage.py runserver
```

### Step 9: Access Admin Panel
- Open browser: http://localhost:8000/admin
- Login with superuser credentials

## ✅ What's Been Set Up

### 1. Admin Panel App (Modular) ✅
- All admin code in `admin_panel` app
- Clean separation of concerns
- Easy to maintain

### 2. Consolidated CSS ✅
- All admin CSS in `static/admin/css/admin.css`
- Comprehensive styling
- Responsive design

### 3. Consolidated JavaScript ✅
- All admin JS in `static/admin/js/admin.js`
- Enhanced features
- Better UX

### 4. Environment Configuration ✅
- `.env` file for configuration
- Security settings
- Database settings
- Email settings

### 5. Database Setup ✅
- PostgreSQL configuration
- Setup scripts
- Management scripts

## 🔧 Database Management

### Quick Commands
```bash
# Start PostgreSQL
./manage_db.sh start

# Run migrations
./manage_db.sh migrate

# Create superuser
./manage_db.sh createsuperuser

# Backup database
./manage_db.sh backup

# Restore database
./manage_db.sh restore backup_file.sql
```

## 🔒 Security Checklist

- [ ] Update `SECRET_KEY` in `.env`
- [ ] Set strong database password
- [ ] Change `ADMIN_URL` (optional)
- [ ] Set `ADMIN_IP_WHITELIST` (optional)
- [ ] Configure email settings
- [ ] Set `DEBUG=False` in production
- [ ] Enable SSL in production

## 📚 Documentation

- `ADMIN_SETUP.md` - Admin panel details
- `SETUP_COMPLETE.md` - Complete setup guide
- `SECURITY.md` - Security configuration
- `DOCKER.md` - Docker setup
- `README.md` - Project overview

## 🆘 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
sudo -u postgres psql -l | grep parsajournal_db

# Test connection
psql -h localhost -U postgres -d parsajournal_db
```

### Migration Errors
```bash
# Make sure database exists
# Check .env file has correct database credentials
# Run makemigrations first
python manage.py makemigrations
python manage.py migrate
```

### Admin Panel Not Loading
```bash
# Check admin_panel is in INSTALLED_APPS
# Check middleware is configured
# Check URLs are configured
# Check logs: tail -f logs/django.log
```

## 🎉 Ready to Go!

Your Parsa Journal website is ready! Follow the steps above to get started.

For detailed information, see the documentation files.

