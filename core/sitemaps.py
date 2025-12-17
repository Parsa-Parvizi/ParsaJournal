from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from articles.models import Article, Category
from reviews.models import BookReview, MovieReview


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Article.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Category.objects.all()


class BookReviewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return BookReview.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class MovieReviewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return MovieReview.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['core:home', 'core:about', 'core:contact', 'articles:article_list', 'reviews:book_list', 'reviews:movie_list']

    def location(self, item):
        return reverse(item)

