from django.contrib import admin
from .models import BookReview, MovieReview, BookCategory, MovieCategory
from articles.widgets import RichTextareaWidget


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'book_title', 'book_author', 'author', 'category', 'rating', 'is_featured', 'is_published', 'published_at', 'views']
    list_filter = ['category', 'rating', 'is_featured', 'is_published', 'language', 'published_at', 'created_at']
    search_fields = ['title', 'book_title', 'book_author', 'author__display_name', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'views']
    date_hierarchy = 'published_at'
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = RichTextareaWidget(attrs={'rows': 25})
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'language')
        }),
        ('Book Details', {
            'fields': ('book_title', 'book_author', 'book_isbn', 'book_year', 'rating', 'purchase_link')
        }),
        ('Review Content', {
            'fields': ('excerpt', 'content', 'cover_image', 'image_alt')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status & Visibility', {
            'fields': ('is_featured', 'is_published', 'published_at')
        }),
        ('Statistics', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'language', 'created_at']
    list_filter = ['language', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'language', 'description', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


class MovieCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'language', 'created_at']
    list_filter = ['language', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'language', 'description', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


class MovieReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie_title', 'director', 'author', 'category', 'rating', 'is_featured', 'is_published', 'published_at', 'views']
    list_filter = ['category', 'rating', 'is_featured', 'is_published', 'language', 'year', 'published_at', 'created_at']
    search_fields = ['title', 'movie_title', 'director', 'author__display_name', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'views']
    date_hierarchy = 'published_at'
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = RichTextareaWidget(attrs={'rows': 25})
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'language')
        }),
        ('Movie Details', {
            'fields': ('movie_title', 'director', 'year', 'genre', 'rating', 'watch_link')
        }),
        ('Review Content', {
            'fields': ('excerpt', 'content', 'poster_image', 'image_alt')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status & Visibility', {
            'fields': ('is_featured', 'is_published', 'published_at')
        }),
        ('Statistics', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
