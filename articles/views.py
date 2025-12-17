from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .models import Article, Category, Tag
from comments.models import Comment
from comments.forms import CommentForm


def article_list(request):
    """List all published articles with pagination"""
    current_language = request.LANGUAGE_CODE
    articles = Article.objects.filter(status='published', language=current_language).select_related('author', 'category').prefetch_related('tags')
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=category)
    else:
        category = None
    
    # Filter by tag
    tag_slug = request.GET.get('tag')
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = articles.filter(tags=tag)
    else:
        tag = None
    
    # Search
    search_query = request.GET.get('q')
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories and tags for sidebar (filtered by language)
    # Show categories that have articles in the current language
    categories = Category.objects.filter(
        articles__language=current_language,
        articles__status='published'
    ).distinct().annotate(
        article_count=Count('articles', filter=Q(articles__language=current_language, articles__status='published'))
    ).filter(article_count__gt=0).order_by('-article_count')[:10]
    
    tags = Tag.objects.filter(
        articles__language=current_language,
        articles__status='published'
    ).distinct().annotate(
        article_count=Count('articles', filter=Q(articles__language=current_language, articles__status='published'))
    ).filter(article_count__gt=0).order_by('-article_count')[:20]
    
    context = {
        'page_obj': page_obj,
        'category': category,
        'tag': tag,
        'search_query': search_query,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'articles/article_list.html', context)


def article_detail(request, slug):
    """Article detail page with comments"""
    current_language = request.LANGUAGE_CODE
    article = get_object_or_404(Article.objects.select_related('author', 'category').prefetch_related('tags'), slug=slug, status='published', language=current_language)
    
    # Increment views
    article.increment_views()
    
    # Get related articles
    related_articles = Article.objects.filter(
        category=article.category,
        status='published',
        language=current_language
    ).exclude(id=article.id).select_related('author')[:3]
    
    # Get comments
    article_content_type = ContentType.objects.get_for_model(Article)
    comments = Comment.objects.filter(
        content_type=article_content_type,
        object_id=article.id,
        is_approved=True,
        parent__isnull=True
    ).select_related('user').prefetch_related('replies')
    
    # Handle comment form
    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_type = ContentType.objects.get_for_model(Article)
            comment.object_id = article.id
            if request.user.is_authenticated:
                comment.user = request.user
                comment.name = request.user.get_full_name() or request.user.username
                comment.email = request.user.email
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting moderation.')
            return redirect('articles:article_detail', slug=slug)
    else:
        form = CommentForm(user=request.user)
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'comments': comments,
        'form': form,
    }
    return render(request, 'articles/article_detail.html', context)


def category_detail(request, slug):
    """Category detail page"""
    current_language = request.LANGUAGE_CODE
    category = get_object_or_404(Category, slug=slug, language=current_language)
    articles = Article.objects.filter(category=category, status='published', language=current_language).select_related('author').prefetch_related('tags')
    
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'articles/category_detail.html', context)


def tag_detail(request, slug):
    """Tag detail page"""
    current_language = request.LANGUAGE_CODE
    tag = get_object_or_404(Tag, slug=slug)
    articles = Article.objects.filter(tags=tag, status='published', language=current_language).select_related('author', 'category').prefetch_related('tags')
    
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'articles/tag_detail.html', context)


def author_detail(request, slug):
    """Author detail page"""
    from accounts.models import Author
    current_language = request.LANGUAGE_CODE
    author = get_object_or_404(Author, slug=slug, is_active=True)
    articles = Article.objects.filter(author=author, status='published', language=current_language).select_related('category').prefetch_related('tags')
    
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'articles/author_detail.html', context)
