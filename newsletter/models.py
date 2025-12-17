from django.db import models
from django.utils import timezone


class NewsletterSubscriber(models.Model):
    """Newsletter Subscription Model"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email

    def unsubscribe(self):
        """Unsubscribe the user from newsletter"""
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save()


class NewsletterCampaign(models.Model):
    """Newsletter Campaign Model"""
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Newsletter Campaign'
        verbose_name_plural = 'Newsletter Campaigns'
        ordering = ['-created_at']

    def __str__(self):
        return self.subject
