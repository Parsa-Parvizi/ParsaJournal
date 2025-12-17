from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_author_name', 'get_content_type', 'content_object', 'is_approved', 'is_spam', 'created_at']
    list_filter = ['is_approved', 'is_spam', 'created_at', 'content_type']
    search_fields = ['name', 'email', 'content', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Comment Details', {
            'fields': ('content_type', 'object_id', 'content_object')
        }),
        ('Author Information', {
            'fields': ('user', 'name', 'email', 'website')
        }),
        ('Content', {
            'fields': ('content', 'parent')
        }),
        ('Status', {
            'fields': ('is_approved', 'is_spam')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_author_name(self, obj):
        return obj.get_author_name()
    get_author_name.short_description = 'Author'

    def get_content_type(self, obj):
        return obj.content_type.model
    get_content_type.short_description = 'Content Type'
