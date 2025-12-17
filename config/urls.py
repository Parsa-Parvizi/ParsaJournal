"""
URL configuration for parsajournal.ir project.
"""
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, register_converter
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from core.sitemaps import ArticleSitemap, CategorySitemap, BookReviewSitemap, MovieReviewSitemap, StaticViewSitemap
from .converters import UnicodeSlugConverter

# Register custom path converter
register_converter(UnicodeSlugConverter, 'uslug')

# Sitemap configuration
sitemaps = {
    'articles': ArticleSitemap,
    'categories': CategorySitemap,
    'books': BookReviewSitemap,
    'movies': MovieReviewSitemap,
    'static': StaticViewSitemap,
}

# URLs that should not be localized (admin, sitemap, etc.)
urlpatterns = [
    # Custom Admin Panel (replaces Django default admin)
    path('admin/', include('admin_panel.urls')),
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # Language switcher
    path('i18n/setlang/', set_language, name='set_language'),
]

# Localized URLs
urlpatterns += i18n_patterns(
    # Core URLs
    path('', include('core.urls')),
    path('articles/', include('articles.urls')),
    path('reviews/', include('reviews.urls')),
    prefix_default_language=False,  # Don't prefix default language (en)
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
