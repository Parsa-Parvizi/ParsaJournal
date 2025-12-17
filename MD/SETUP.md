# Setup Guide for Parsa Journal

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL Database**
   
   Make sure PostgreSQL is installed and running. Then create the database:
   ```bash
   # Connect to PostgreSQL
   sudo -u postgres psql
   
   # Create database
   CREATE DATABASE parsajournal_db;
   CREATE USER parsauser WITH PASSWORD 'your_password';
   ALTER ROLE parsauser SET client_encoding TO 'utf8';
   ALTER ROLE parsauser SET default_transaction_isolation TO 'read committed';
   ALTER ROLE parsauser SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE parsajournal_db TO parsauser;
   \q
   ```
   
   Update `config/settings.py` with your database credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'parsajournal_db',
           'USER': 'parsauser',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

6. **Run Server**
   ```bash
   python manage.py runserver
   ```

7. **Access Admin Panel**
   - Go to http://127.0.0.1:8000/admin
   - Login with your superuser credentials

## Initial Configuration

1. **Configure Site Settings**
   - Go to Admin → Site Settings
   - Set site name, tagline, description
   - Add contact information
   - Add social media links
   - Configure SEO settings

2. **Create Author Profile**
   - Go to Admin → Authors
   - Create an author profile linked to your user account
   - Add bio, profile image, and social media links

3. **Create Categories**
   - Go to Admin → Articles → Categories
   - Create categories for organizing articles (e.g., "Politics", "Culture", "Technology")

4. **Create Tags**
   - Go to Admin → Articles → Tags
   - Create tags for better categorization

5. **Publish Your First Article**
   - Go to Admin → Articles → Articles
   - Create a new article
   - Set title, content, featured image
   - Select category, tags, and author
   - Set status to "Published"
   - Click Save

## Environment Variables (Optional)

For production, set these environment variables:

```bash
export SECRET_KEY='your-secret-key-here'
export DB_NAME='parsajournal_db'
export DB_USER='parsauser'
export DB_PASSWORD='your-password'
export DB_HOST='localhost'
export DB_PORT='5432'
export EMAIL_HOST='smtp.gmail.com'
export EMAIL_PORT='587'
export EMAIL_HOST_USER='your-email@gmail.com'
export EMAIL_HOST_PASSWORD='your-app-password'
export DEFAULT_FROM_EMAIL='noreply@parsajournal.ir'
```

## Testing

1. **Test Home Page**
   - Visit http://127.0.0.1:8000
   - Verify articles and reviews are displayed

2. **Test Article Pages**
   - Visit http://127.0.0.1:8000/articles/
   - Click on an article to view detail page
   - Test comment functionality

3. **Test Review Pages**
   - Visit http://127.0.0.1:8000/reviews/books/
   - Visit http://127.0.0.1:8000/reviews/movies/
   - Test review detail pages

4. **Test Search**
   - Use the search form in the header
   - Verify search results

5. **Test Newsletter**
   - Subscribe via footer form
   - Verify subscription in Admin → Newsletter → Newsletter Subscribers

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check database credentials in `config/settings.py`
- Verify database exists: `psql -U parsauser -d parsajournal_db`

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` in settings
- Verify `DEBUG = True` for development

### CKEditor Not Working
- Verify `django-ckeditor` is installed: `pip list | grep ckeditor`
- Check CKEditor URLs are included in `config/urls.py`
- Clear browser cache

### Images Not Displaying
- Check `MEDIA_ROOT` and `MEDIA_URL` in settings
- Verify media files are uploaded to correct directory
- Check file permissions: `chmod -R 755 media/`

## Production Deployment

1. **Set DEBUG = False** in `config/settings.py`
2. **Set ALLOWED_HOSTS** to your domain
3. **Set up proper SECRET_KEY** as environment variable
4. **Configure static file serving** (e.g., WhiteNoise or Nginx)
5. **Set up SSL certificate** (Let's Encrypt)
6. **Configure email settings** for newsletter and contact forms
7. **Set up database backups**
8. **Configure logging**

## Support

For issues or questions, refer to the README.md or contact through the website contact form.

