# Parsa Journal

A Django-based journalism website for publishing articles, book reviews, and movie reviews.

## Features

- **Articles Management**: Publish and manage journalistic articles with categories, tags, and images
- **Book Reviews**: Share book recommendations with ratings
- **Movie Reviews**: Share movie recommendations with ratings
- **Rich Text Editor**: CKEditor integration for content creation
- **SEO-Friendly**: Slug-based URLs, meta tags, and sitemap
- **Comment System**: Comment system for articles and reviews
- **Newsletter**: Email subscription management
- **Custom User Model**: Extended user model with author profiles
- **Search Functionality**: Search across articles and reviews
- **Pagination**: Paginated listings for better performance
- **Responsive Design**: Custom CSS (no Bootstrap/Tailwind)

## Technology Stack

- Django 5.2.8
- PostgreSQL
- CKEditor
- Pillow (for image handling)
- Custom CSS

## Installation

1. **Clone the repository**
   ```bash
   cd /home/codus/Journal
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   - Create a PostgreSQL database named `parsajournal_db`
   - Update database settings in `config/settings.py` if needed:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'parsajournal_db',
             'USER': 'postgres',
             'PASSWORD': 'postgres',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the website**
   - Website: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin

## Project Structure

```
Journal/
├── config/              # Django project settings
├── core/                # Core app (home, about, contact, SEO)
├── accounts/            # Custom user and author profiles
├── articles/            # Article management
├── reviews/             # Book and movie reviews
├── newsletter/          # Email subscription
├── comments/            # Comment system
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User uploaded files
└── manage.py
```

## Apps

### Core
- Home page with latest articles and featured reviews
- About page
- Contact page with form
- Search functionality
- Site settings management

### Accounts
- Custom user model
- Author profiles with social media links
- User authentication

### Articles
- Article management with categories and tags
- Rich text editor integration
- Featured images
- SEO meta tags
- Author pages
- Category and tag pages

### Reviews
- Book reviews with ratings
- Movie reviews with ratings
- Purchase/watch links
- Featured reviews

### Newsletter
- Email subscription management
- Newsletter campaigns

### Comments
- Generic comment system for articles and reviews
- Comment moderation
- Nested comments support

## Configuration

### Environment Variables

Set the following environment variables for production:

```bash
SECRET_KEY=your-secret-key
DB_NAME=parsajournal_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@parsajournal.ir
```

### Site Settings

Configure site settings through the admin panel:
- Site name and tagline
- Contact information
- Social media links
- About page content
- SEO settings

## Usage

1. **Create an Author Profile**
   - Go to Admin → Authors
   - Create an author profile linked to a user account

2. **Create Categories and Tags**
   - Go to Admin → Articles → Categories
   - Create categories for organizing articles
   - Create tags for better categorization

3. **Publish Articles**
   - Go to Admin → Articles → Articles
   - Create a new article with title, content, featured image
   - Set category, tags, and author
   - Set status to "Published"

4. **Add Book/Movie Reviews**
   - Go to Admin → Reviews → Book Reviews or Movie Reviews
   - Create reviews with ratings, images, and content
   - Set as featured if needed

5. **Manage Comments**
   - Comments require moderation
   - Go to Admin → Comments to approve/disapprove comments

6. **Newsletter Subscriptions**
   - Subscribers can subscribe via footer form
   - Manage subscriptions in Admin → Newsletter → Newsletter Subscribers

## SEO Features

- Slug-based URLs for all content
- Meta titles and descriptions
- Sitemap at `/sitemap.xml`
- Structured data ready
- SEO-friendly HTML structure

## Security

- CSRF protection enabled
- Secure password validation
- Admin panel access control
- Comment moderation
- Image upload validation

## Customization

### Styling
- Custom CSS in `static/css/style.css`
- No Bootstrap or Tailwind dependencies
- Fully customizable design

### Templates
- Base template: `templates/base.html`
- App-specific templates in respective app folders
- Easy to customize and extend

## License

This project is for personal use.

## Support

For issues or questions, please contact through the contact form on the website.

