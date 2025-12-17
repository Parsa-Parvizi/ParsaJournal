from django.contrib import admin
from .models import NewsletterSubscriber, NewsletterCampaign


class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']
    date_hierarchy = 'subscribed_at'


@admin.register(NewsletterCampaign)
class NewsletterCampaignAdmin(admin.ModelAdmin):
    list_display = ['subject', 'is_sent', 'sent_at', 'created_at']
    list_filter = ['is_sent', 'created_at']
    search_fields = ['subject', 'content']
    readonly_fields = ['created_at', 'sent_at']
