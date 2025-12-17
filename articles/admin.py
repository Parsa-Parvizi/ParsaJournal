from django.contrib import admin
from .models import Category, Tag, Article
from .widgets import RichTextareaWidget


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'language', 'created_at']
    list_filter = ['language', 'created_at']
    search_fields = ['name']
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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'published_at', 'views']
    list_filter = ['status', 'is_featured', 'category', 'tags', 'language', 'published_at', 'created_at']
    search_fields = ['title', 'excerpt', 'content', 'author__display_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'views']
    filter_horizontal = ['tags']
    date_hierarchy = 'published_at'
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = RichTextareaWidget(attrs={'rows': 25})
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'tags', 'language')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image', 'image_alt')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status & Visibility', {
            'fields': ('status', 'is_featured', 'published_at')
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
