"""
Custom Admin Panel Views for Parsa Journal
Comprehensive admin panel with article management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.db.models.functions import TruncDate, TruncDay, TruncMonth
from django.utils import timezone
from django.http import JsonResponse
from django.db import transaction
from datetime import timedelta, datetime
import json

from articles.models import Article, Category, Tag
from reviews.models import BookReview, MovieReview, BookCategory, MovieCategory
from accounts.models import Author
from core.models import ContactMessage
from newsletter.models import NewsletterSubscriber
from comments.models import Comment
from .forms import ArticleForm, CategoryForm, TagForm


def is_superuser(user):
    """Check if user is superuser"""
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(is_superuser, login_url='core:login')
def dashboard(request):
    """Admin Dashboard with statistics and overview"""
    # Get statistics for all content types
    total_articles = Article.objects.count()
    published_articles = Article.objects.filter(status='published').count()
    draft_articles = Article.objects.filter(status='draft').count()
    featured_articles = Article.objects.filter(is_featured=True).count()
    
    # Book reviews statistics
    total_book_reviews = BookReview.objects.count()
    published_book_reviews = BookReview.objects.filter(is_published=True).count()
    featured_book_reviews = BookReview.objects.filter(is_featured=True).count()
    
    # Movie reviews statistics
    total_movie_reviews = MovieReview.objects.count()
    published_movie_reviews = MovieReview.objects.filter(is_published=True).count()
    featured_movie_reviews = MovieReview.objects.filter(is_featured=True).count()
    
    # Get total views (all content types)
    article_views = Article.objects.aggregate(total=Sum('views'))['total'] or 0
    book_views = BookReview.objects.aggregate(total=Sum('views'))['total'] or 0
    movie_views = MovieReview.objects.aggregate(total=Sum('views'))['total'] or 0
    total_views = article_views + book_views + movie_views
    
    # Get recent content (all types)
    recent_articles = Article.objects.select_related('author', 'category').order_by('-created_at')[:5]
    recent_books = BookReview.objects.select_related('author', 'category').order_by('-created_at')[:5]
    recent_movies = MovieReview.objects.select_related('author', 'category').order_by('-created_at')[:5]
    
    # Get articles by status
    articles_by_status = Article.objects.values('status').annotate(count=Count('id'))
    
    # Get articles by date (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_articles_count = Article.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # Get popular content (by views) - all types
    popular_articles = Article.objects.select_related('author', 'category').order_by('-views')[:5]
    popular_books = BookReview.objects.select_related('author', 'category').order_by('-views')[:5]
    popular_movies = MovieReview.objects.select_related('author', 'category').order_by('-views')[:5]
    
    # Get contact messages
    new_messages = ContactMessage.objects.filter(status='new').count()
    total_messages = ContactMessage.objects.count()
    
    # Get newsletter subscribers
    total_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()
    
    # Get comments
    pending_comments = Comment.objects.filter(is_approved=False).count()
    total_comments = Comment.objects.count()
    
    # Get categories and tags counts
    categories_count = Category.objects.count()
    tags_count = Tag.objects.count()
    book_categories_count = BookCategory.objects.count()
    movie_categories_count = MovieCategory.objects.count()
    
    context = {
        'total_articles': total_articles,
        'published_articles': published_articles,
        'draft_articles': draft_articles,
        'featured_articles': featured_articles,
        'total_book_reviews': total_book_reviews,
        'published_book_reviews': published_book_reviews,
        'featured_book_reviews': featured_book_reviews,
        'total_movie_reviews': total_movie_reviews,
        'published_movie_reviews': published_movie_reviews,
        'featured_movie_reviews': featured_movie_reviews,
        'total_views': total_views,
        'recent_articles': recent_articles,
        'recent_books': recent_books,
        'recent_movies': recent_movies,
        'articles_by_status': articles_by_status,
        'recent_articles_count': recent_articles_count,
        'popular_articles': popular_articles,
        'popular_books': popular_books,
        'popular_movies': popular_movies,
        'new_messages': new_messages,
        'total_messages': total_messages,
        'total_subscribers': total_subscribers,
        'pending_comments': pending_comments,
        'total_comments': total_comments,
        'categories_count': categories_count,
        'tags_count': tags_count,
        'book_categories_count': book_categories_count,
        'movie_categories_count': movie_categories_count,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@user_passes_test(is_superuser, login_url='core:login')
def article_list(request):
    """Content list with search, filter, and pagination - includes articles, books, and movies"""
    content_type = request.GET.get('type', 'all')  # all, article, book, movie
    
    # Base querysets
    articles_qs = Article.objects.select_related('author', 'category').prefetch_related('tags').all()
    books_qs = BookReview.objects.select_related('author', 'category').all()
    movies_qs = MovieReview.objects.select_related('author', 'category').all()
    
    # Search
    search_query = request.GET.get('q', '').strip()
    if search_query:
        articles_qs = articles_qs.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__display_name__icontains=search_query)
        )
        books_qs = books_qs.filter(
            Q(title__icontains=search_query) |
            Q(book_title__icontains=search_query) |
            Q(book_author__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(author__display_name__icontains=search_query)
        )
        movies_qs = movies_qs.filter(
            Q(title__icontains=search_query) |
            Q(movie_title__icontains=search_query) |
            Q(director__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(author__display_name__icontains=search_query)
        )
    
    # Filter by content type
    if content_type == 'article':
        all_content = list(articles_qs)
    elif content_type == 'book':
        all_content = list(books_qs)
    elif content_type == 'movie':
        all_content = list(movies_qs)
    else:
        # Combine all content types
        all_content = list(articles_qs) + list(books_qs) + list(movies_qs)
    
    # Filter by status (for articles)
    status_filter = request.GET.get('status', '')
    if status_filter and content_type in ['all', 'article']:
        all_content = [item for item in all_content if hasattr(item, 'status') and item.status == status_filter]
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        if content_type == 'article':
            all_content = [item for item in all_content if hasattr(item, 'category') and item.category and str(item.category.id) == category_filter]
        elif content_type == 'book':
            all_content = [item for item in all_content if hasattr(item, 'category') and item.category and str(item.category.id) == category_filter]
        elif content_type == 'movie':
            all_content = [item for item in all_content if hasattr(item, 'category') and item.category and str(item.category.id) == category_filter]
        else:
            all_content = [item for item in all_content if hasattr(item, 'category') and item.category and str(item.category.id) == category_filter]
    
    # Filter by featured
    featured_filter = request.GET.get('featured', '')
    if featured_filter == 'yes':
        all_content = [item for item in all_content if hasattr(item, 'is_featured') and item.is_featured]
    elif featured_filter == 'no':
        all_content = [item for item in all_content if hasattr(item, 'is_featured') and not item.is_featured]
    
    # Sort all content
    order_by = request.GET.get('order_by', '-created_at')
    reverse_order = order_by.startswith('-')
    sort_field = order_by.lstrip('-')
    
    def get_sort_value(item):
        if sort_field == 'created_at':
            return item.created_at if hasattr(item, 'created_at') else timezone.now()
        elif sort_field == 'published_at':
            return item.published_at if hasattr(item, 'published_at') and item.published_at else timezone.now()
        elif sort_field == 'views':
            return item.views if hasattr(item, 'views') else 0
        elif sort_field == 'title':
            return item.title.lower() if hasattr(item, 'title') else ''
        else:
            return item.created_at if hasattr(item, 'created_at') else timezone.now()
    
    all_content.sort(key=get_sort_value, reverse=reverse_order)
    
    # Pagination
    paginator = Paginator(all_content, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter
    categories = Category.objects.all()
    book_categories = BookCategory.objects.all()
    movie_categories = MovieCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'articles': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'featured_filter': featured_filter,
        'order_by': order_by,
        'content_type': content_type,
        'categories': categories,
        'book_categories': book_categories,
        'movie_categories': movie_categories,
        'status_choices': Article.STATUS_CHOICES,
    }
    return render(request, 'admin_panel/article_list.html', context)


@login_required
@user_passes_test(is_superuser, login_url='core:login')
def article_create(request):
    """Create new article"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'Article "{article.title}" has been created successfully.')
            return redirect('admin_panel:article_list')
    else:
        form = ArticleForm()
    
    # Get authors and categories for form
    authors = Author.objects.filter(is_active=True)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'form': form,
        'authors': authors,
        'categories': categories,
        'tags': tags,
        'action': 'create',
    }
    return render(request, 'admin_panel/article_form.html', context)


@login_required
@user_passes_test(is_superuser, login_url='core:login')
def article_edit(request, pk):
    """Edit existing article"""
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'Article "{article.title}" has been updated successfully.')
            return redirect('admin_panel:article_list')
    else:
        form = ArticleForm(instance=article)
    
    # Get authors and categories for form
    authors = Author.objects.filter(is_active=True)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'form': form,
        'article': article,
        'authors': authors,
        'categories': categories,
        'tags': tags,
        'action': 'edit',
    }
    return render(request, 'admin_panel/article_form.html', context)


@login_required
@user_passes_test(is_superuser, login_url='core:login')
def article_delete(request, pk):
    """Delete article"""
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        article_title = article.title
        article.delete()
        messages.success(request, f'Article "{article_title}" has been deleted successfully.')
        return redirect('admin_panel:article_list')
    
    context = {
        'article': article,
    }
    return render(request, 'admin_panel/article_delete.html', context)


@login_required
@user_passes_test(is_superuser, login_url='core:login')
def article_detail(request, pk):
    """View article details"""
    article = get_object_or_404(
        Article.objects.select_related('author', 'category').prefetch_related('tags'),
        pk=pk
    )
    
    context = {
        'article': article,
    }
    return render(request, 'admin_panel/article_detail.html', context)


@login_required
@user_passes_test(is_superuser, login_url='core:login')
def article_toggle_featured(request, pk):
    """Toggle article featured status"""
    article = get_object_or_404(Article, pk=pk)
    article.is_featured = not article.is_featured
    article.save()
    
    status = 'featured' if article.is_featured else 'removed from featured'
    messages.success(request, f'Article "{article.title}" has been {status}.')
    return redirect('admin_panel:article_list')


@login_required
@user_passes_test(is_superuser, login_url='core:login')
def article_change_status(request, pk):
    """Change article status"""
    article = get_object_or_404(Article, pk=pk)
    new_status = request.POST.get('status', '')
    
    if new_status in [choice[0] for choice in Article.STATUS_CHOICES]:
        article.status = new_status
        if new_status == 'published' and not article.published_at:
            article.published_at = timezone.now()
        article.save()
        messages.success(request, f'Article "{article.title}" status has been changed to "{article.get_status_display()}".')
    
    return redirect('admin_panel:article_list')


@login_required
@user_passes_test(is_superuser, login_url='core:login')
def article_bulk_delete(request):
    """Bulk delete articles"""
    if request.method == 'POST':
        article_ids = request.POST.getlist('article_ids')
        if article_ids:
            articles = Article.objects.filter(pk__in=article_ids)
            count = articles.count()
            articles.delete()
            messages.success(request, f'{count} article(s) have been deleted successfully.')
        else:
            messages.warning(request, 'No articles were selected.')
    
    return redirect('admin_panel:article_list')


@login_required
@user_passes_test(is_superuser, login_url='core:login')
def statistics(request):
    """Detailed statistics and reports"""
    # Article statistics
    total_articles = Article.objects.count()
    published_articles = Article.objects.filter(status='published').count()
    draft_articles = Article.objects.filter(status='draft').count()
    archived_articles = Article.objects.filter(status='archived').count()
    
    # Views statistics
    total_views = Article.objects.aggregate(total=Sum('views'))['total'] or 0
    articles_with_views = Article.objects.filter(views__gt=0)
    avg_views = round(total_views / articles_with_views.count(), 2) if articles_with_views.count() > 0 else 0
    
    # Articles by date (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    articles_by_date = Article.objects.filter(
        created_at__gte=thirty_days_ago
    ).extra(
        select={'date': 'DATE(created_at)'}
    ).values('date').annotate(count=Count('id')).order_by('date')
    
    # Top articles by views
    top_articles = Article.objects.select_related('author', 'category').order_by('-views')[:10]
    
    # Articles by category
    articles_by_category = Category.objects.annotate(
        article_count=Count('articles')
    ).order_by('-article_count')
    
    # Articles by author
    articles_by_author = Author.objects.annotate(
        article_count=Count('articles')
    ).order_by('-article_count')[:10]
    
    # Recent activity
    recent_articles = Article.objects.select_related('author', 'category').order_by('-created_at')[:10]
    
    context = {
        'total_articles': total_articles,
        'published_articles': published_articles,
        'draft_articles': draft_articles,
        'archived_articles': archived_articles,
        'total_views': total_views,
        'avg_views': round(avg_views, 2),
        'articles_by_date': articles_by_date,
        'top_articles': top_articles,
        'articles_by_category': articles_by_category,
        'articles_by_author': articles_by_author,
        'recent_articles': recent_articles,
    }
    return render(request, 'admin_panel/statistics.html', context)


@login_required
@user_passes_test(is_superuser, login_url='core:login')
def chart_data(request):
    """API endpoint for chart data"""
    # Get date range from request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    period = request.GET.get('period', 'day')  # day, week, month
    
    # Default to last 30 days if not provided
    if not end_date:
        end_date = timezone.now()
    else:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            end_date = timezone.make_aware(end_date)
        except:
            end_date = timezone.now()
    
    if not start_date:
        start_date = end_date - timedelta(days=30)
    else:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date)
        except:
            start_date = end_date - timedelta(days=30)
    
    # Determine truncation based on period
    if period == 'month':
        trunc_func = TruncMonth('created_at')
    elif period == 'week':
        trunc_func = TruncDate('created_at')
    else:  # day
        trunc_func = TruncDate('created_at')
    
    # Get articles data grouped by date
    articles_data = Article.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date
    ).annotate(
        date=trunc_func
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    # Get views data grouped by date (using published_at or created_at)
    views_data = Article.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date
    ).annotate(
        date=trunc_func
    ).values('date').annotate(
        total_views=Sum('views')
    ).order_by('date')
    
    # Format data for charts
    articles_labels = []
    articles_counts = []
    views_labels = []
    views_totals = []
    
    # Create dictionaries from queryset data
    articles_dict = {}
    for item in articles_data:
        if item['date']:
            if period == 'month':
                key = item['date'].date().replace(day=1)
            else:
                key = item['date'].date()
            articles_dict[key] = item['count']
    
    views_dict = {}
    for item in views_data:
        if item['date']:
            if period == 'month':
                key = item['date'].date().replace(day=1)
            else:
                key = item['date'].date()
            views_dict[key] = item['total_views'] or 0
    
    # Create a complete date range
    current_date = start_date
    
    if period == 'month':
        # For monthly, group by month
        current_date = current_date.replace(day=1)
        while current_date <= end_date:
            month_key = current_date.date().replace(day=1)
            articles_labels.append(month_key.strftime('%Y-%m'))
            articles_counts.append(articles_dict.get(month_key, 0))
            views_labels.append(month_key.strftime('%Y-%m'))
            views_totals.append(views_dict.get(month_key, 0))
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)
            if current_date > end_date:
                break
    else:
        # For daily/weekly
        while current_date <= end_date:
            date_key = current_date.date()
            date_str = current_date.strftime('%Y-%m-%d')
            articles_labels.append(date_str)
            articles_counts.append(articles_dict.get(date_key, 0))
            views_labels.append(date_str)
            views_totals.append(views_dict.get(date_key, 0))
            current_date += timedelta(days=1)
    
    return JsonResponse({
        'articles': {
            'labels': articles_labels,
            'data': articles_counts
        },
        'views': {
            'labels': views_labels,
            'data': views_totals
        },
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'period': period
    })

