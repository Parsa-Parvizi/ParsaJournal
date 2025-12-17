from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Article Category Model"""
    LANGUAGE_CHOICES = [
        ('fa', 'Persian'),
        ('en', 'English'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fa', help_text='Category language')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        unique_together = [['slug', 'language']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('articles:category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Article Tag Model"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('articles:tag_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    """Journalistic Article Model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    LANGUAGE_CHOICES = [
        ('fa', 'Persian'),
        ('en', 'English'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey('accounts.Author', on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fa', help_text='Article language')
    
    # Content
    excerpt = models.TextField(max_length=500, help_text='Short summary of the article')
    content = models.TextField(help_text='Article content (HTML supported)')
    
    # Images
    featured_image = models.ImageField(upload_to='articles/', blank=True, null=True, help_text='Main image for the article')
    image_alt = models.CharField(max_length=200, blank=True, help_text='Alt text for featured image')
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, help_text='SEO title (optional)')
    meta_description = models.TextField(max_length=300, blank=True, help_text='SEO description (optional)')
    
    # Status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at', 'status']),
            models.Index(fields=['slug']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        # Auto-set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def increment_views(self):
        """Increment article view count"""
        self.views += 1
        self.save(update_fields=['views'])
