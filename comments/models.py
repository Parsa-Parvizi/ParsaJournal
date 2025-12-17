from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Comment(models.Model):
    """Generic Comment Model for Articles and Reviews"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    name = models.CharField(max_length=100, help_text='Name if user is not logged in')
    email = models.EmailField(help_text='Email if user is not logged in')
    website = models.URLField(blank=True)
    
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    
    # For nested comments
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['is_approved']),
        ]

    def __str__(self):
        author_name = self.user.username if self.user else self.name
        return f"Comment by {author_name} on {self.content_object}"

    def get_author_name(self):
        """Get author name (user or name field)"""
        return self.user.get_full_name() or self.user.username if self.user else self.name

    def get_author_email(self):
        """Get author email (user or email field)"""
        return self.user.email if self.user else self.email
