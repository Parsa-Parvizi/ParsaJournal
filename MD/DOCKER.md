# Docker Setup Guide for Parsa Journal

## Prerequisites

- Docker installed on your system
- Docker Compose installed
- `.env` file configured (see `.env.example`)

## Quick Start

### Development Mode

1. **Start services:**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **Run migrations:**
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
   ```

4. **Collect static files:**
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput
   ```

5. **Access the application:**
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin (or your custom ADMIN_URL)

### Production Mode

1. **Build and start services:**
   ```bash
   docker-compose up -d --build
   ```

2. **Run migrations:**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Collect static files:**
   ```bash
   docker-compose exec web python manage.py collectstatic --noinput
   ```

5. **Access the application:**
   - Website: http://localhost:80 (or your domain)
   - Admin: http://localhost:80/admin (or your custom ADMIN_URL)

## Docker Commands

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
```

### Stop services
```bash
docker-compose down
```

### Stop and remove volumes (CAUTION: This deletes database data)
```bash
docker-compose down -v
```

### Restart services
```bash
docker-compose restart
```

### Execute commands in container
```bash
# Django shell
docker-compose exec web python manage.py shell

# Database shell
docker-compose exec db psql -U postgres -d parsajournal_db

# Bash shell
docker-compose exec web bash
```

### Rebuild containers
```bash
docker-compose up -d --build
```

## Database Management

### Backup database
```bash
docker-compose exec db pg_dump -U postgres parsajournal_db > backup.sql
```

### Restore database
```bash
docker-compose exec -T db psql -U postgres parsajournal_db < backup.sql
```

### Access database directly
```bash
docker-compose exec db psql -U postgres -d parsajournal_db
```

## Nginx Configuration

For production, uncomment the HTTPS server block in `nginx.conf` and configure SSL certificates:

1. Place SSL certificates in `./ssl/` directory:
   - `cert.pem` - SSL certificate
   - `key.pem` - SSL private key

2. Update `nginx.conf` to enable HTTPS

3. Update `.env` to set `SECURE_SSL_REDIRECT=True`

## Environment Variables

Make sure your `.env` file is configured correctly. See `.env.example` for reference.

Important variables:
- `DB_HOST=db` (use service name in Docker)
- `DB_NAME=parsajournal_db`
- `DB_USER=postgres`
- `DB_PASSWORD=your-password`
- `DEBUG=False` (for production)
- `SECRET_KEY=your-secret-key`

## Troubleshooting

### Database connection errors
- Check if database service is running: `docker-compose ps`
- Verify database credentials in `.env`
- Check database logs: `docker-compose logs db`

### Static files not loading
- Run `collectstatic`: `docker-compose exec web python manage.py collectstatic --noinput`
- Check nginx configuration
- Verify volume mounts in `docker-compose.yml`

### Permission issues
```bash
# Fix permissions
docker-compose exec web chmod -R 755 /app/staticfiles
docker-compose exec web chmod -R 755 /app/media
```

### Container won't start
- Check logs: `docker-compose logs web`
- Verify `.env` file exists and is configured
- Check if ports are already in use

## Production Deployment

1. **Set up SSL certificates** (Let's Encrypt recommended)
2. **Configure domain** in `.env` and `nginx.conf`
3. **Set `DEBUG=False`** in `.env`
4. **Set strong `SECRET_KEY`** in `.env`
5. **Configure `ADMIN_IP_WHITELIST`** for admin security
6. **Set up regular database backups**
7. **Configure monitoring and logging**
8. **Set up CI/CD pipeline** (optional)

## Security Checklist

- [ ] Change default admin URL (`ADMIN_URL` in `.env`)
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ADMIN_IP_WHITELIST`
- [ ] Enable HTTPS (SSL certificates)
- [ ] Set `DEBUG=False` in production
- [ ] Configure firewall rules
- [ ] Set up regular backups
- [ ] Enable database encryption
- [ ] Configure rate limiting
- [ ] Set up monitoring and alerts

