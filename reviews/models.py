from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class BookCategory(models.Model):
    """Book Review Category Model"""
    LANGUAGE_CHOICES = [
        ('fa', 'Persian'),
        ('en', 'English'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='book_categories/', blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fa', help_text='Category language')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Book Category'
        verbose_name_plural = 'Book Categories'
        ordering = ['name']
        unique_together = [['slug', 'language']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reviews:book_category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MovieCategory(models.Model):
    """Movie Review Category Model"""
    LANGUAGE_CHOICES = [
        ('fa', 'Persian'),
        ('en', 'English'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='movie_categories/', blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fa', help_text='Category language')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Movie Category'
        verbose_name_plural = 'Movie Categories'
        ordering = ['name']
        unique_together = [['slug', 'language']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reviews:movie_category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BookReview(models.Model):
    """Book Review/Recommendation Model"""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    LANGUAGE_CHOICES = [
        ('fa', 'Persian'),
        ('en', 'English'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey('accounts.Author', on_delete=models.CASCADE, related_name='book_reviews')
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='book_reviews')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en', help_text='Review language')
    
    # Book details
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    book_isbn = models.CharField(max_length=20, blank=True)
    book_year = models.PositiveIntegerField(null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    
    # Review content
    excerpt = models.TextField(max_length=500)
    content = models.TextField(help_text='Review content (HTML supported)')
    
    # Images
    cover_image = models.ImageField(upload_to='book_reviews/', blank=True, null=True, help_text='Book cover image')
    image_alt = models.CharField(max_length=200, blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    
    # Links
    purchase_link = models.URLField(blank=True, help_text='Link to purchase the book')
    
    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Book Review'
        verbose_name_plural = 'Book Reviews'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at', 'is_published']),
            models.Index(fields=['slug']),
            models.Index(fields=['rating']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.title} - {self.book_title}"

    def get_absolute_url(self):
        return reverse('reviews:book_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        if self.is_published and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def increment_views(self):
        """Increment review view count"""
        self.views += 1
        self.save(update_fields=['views'])


class MovieReview(models.Model):
    """Movie Review/Recommendation Model"""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    LANGUAGE_CHOICES = [
        ('fa', 'Persian'),
        ('en', 'English'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey('accounts.Author', on_delete=models.CASCADE, related_name='movie_reviews')
    category = models.ForeignKey(MovieCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='movie_reviews')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en', help_text='Review language')
    
    # Movie details
    movie_title = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    year = models.PositiveIntegerField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    
    # Review content
    excerpt = models.TextField(max_length=500)
    content = models.TextField(help_text='Review content (HTML supported)')
    
    # Images
    poster_image = models.ImageField(upload_to='movie_reviews/', blank=True, null=True, help_text='Movie poster image')
    image_alt = models.CharField(max_length=200, blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    
    # Links
    watch_link = models.URLField(blank=True, help_text='Link to watch the movie')
    
    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Movie Review'
        verbose_name_plural = 'Movie Reviews'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at', 'is_published']),
            models.Index(fields=['slug']),
            models.Index(fields=['rating']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.title} - {self.movie_title}"

    def get_absolute_url(self):
        return reverse('reviews:movie_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        if self.is_published and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def increment_views(self):
        """Increment review view count"""
        self.views += 1
        self.save(update_fields=['views'])
