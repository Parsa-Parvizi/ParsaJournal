"""
Admin Registry - Register all models to custom admin site
This module handles registration of all models to the custom admin site.
"""
from django.contrib.auth.models import Group


def register_all_models():
    """Register all models to the custom admin site"""
    from admin_panel.admin_site import admin_site
    
    # Import admin classes
    from accounts.admin import UserAdmin, AuthorAdmin
    from accounts.models import User, Author
    from articles.admin import ArticleAdmin, CategoryAdmin, TagAdmin
    from articles.models import Article, Category, Tag
    from reviews.admin import BookReviewAdmin, MovieReviewAdmin, BookCategoryAdmin, MovieCategoryAdmin
    from reviews.models import BookReview, MovieReview, BookCategory, MovieCategory
    from newsletter.admin import NewsletterSubscriberAdmin, NewsletterCampaignAdmin
    from newsletter.models import NewsletterSubscriber, NewsletterCampaign
    from comments.admin import CommentAdmin
    from comments.models import Comment
    from core.admin import SiteSettingsAdmin, ContactMessageAdmin
    from core.models import SiteSettings, ContactMessage
    
    # Register models
    admin_site.register(User, UserAdmin)
    admin_site.register(Author, AuthorAdmin)
    admin_site.register(Article, ArticleAdmin)
    admin_site.register(Category, CategoryAdmin)
    admin_site.register(Tag, TagAdmin)
    admin_site.register(BookReview, BookReviewAdmin)
    admin_site.register(MovieReview, MovieReviewAdmin)
    admin_site.register(BookCategory, BookCategoryAdmin)
    admin_site.register(MovieCategory, MovieCategoryAdmin)
    admin_site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
    admin_site.register(NewsletterCampaign, NewsletterCampaignAdmin)
    admin_site.register(Comment, CommentAdmin)
    admin_site.register(SiteSettings, SiteSettingsAdmin)
    admin_site.register(ContactMessage, ContactMessageAdmin)
    admin_site.register(Group)

