from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .models import BookReview, MovieReview, BookCategory, MovieCategory
from comments.models import Comment
from comments.forms import CommentForm


def book_list(request):
    """List all published book reviews"""
    current_language = request.LANGUAGE_CODE
    books = BookReview.objects.filter(is_published=True, language=current_language).select_related('author', 'category')
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(BookCategory, slug=category_slug)
        books = books.filter(category=category)
    else:
        category = None
    
    # Filter by rating
    rating = request.GET.get('rating')
    if rating:
        books = books.filter(rating=rating)
    
    # Get all categories for filter (filtered by language)
    categories = BookCategory.objects.filter(language=current_language)
    
    # Pagination
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'rating': rating,
        'category': category,
        'categories': categories,
    }
    return render(request, 'reviews/book_list.html', context)


def book_detail(request, slug):
    """Book review detail page"""
    current_language = request.LANGUAGE_CODE
    book = get_object_or_404(BookReview.objects.select_related('author'), slug=slug, is_published=True, language=current_language)
    
    # Increment views
    book.increment_views()
    
    # Get related books
    related_books = BookReview.objects.filter(
        is_published=True,
        language=current_language
    ).exclude(id=book.id).select_related('author')[:3]
    
    # Get comments
    book_content_type = ContentType.objects.get_for_model(BookReview)
    comments = Comment.objects.filter(
        content_type=book_content_type,
        object_id=book.id,
        is_approved=True,
        parent__isnull=True
    ).select_related('user').prefetch_related('replies')
    
    # Handle comment form
    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_type = ContentType.objects.get_for_model(BookReview)
            comment.object_id = book.id
            if request.user.is_authenticated:
                comment.user = request.user
                comment.name = request.user.get_full_name() or request.user.username
                comment.email = request.user.email
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting moderation.')
            return redirect('reviews:book_detail', slug=slug)
    else:
        form = CommentForm(user=request.user)
    
    context = {
        'book': book,
        'related_books': related_books,
        'comments': comments,
        'form': form,
    }
    return render(request, 'reviews/book_detail.html', context)


def movie_list(request):
    """List all published movie reviews"""
    current_language = request.LANGUAGE_CODE
    movies = MovieReview.objects.filter(is_published=True, language=current_language).select_related('author', 'category')
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(MovieCategory, slug=category_slug)
        movies = movies.filter(category=category)
    else:
        category = None
    
    # Filter by rating
    rating = request.GET.get('rating')
    if rating:
        movies = movies.filter(rating=rating)
    
    # Filter by year
    year = request.GET.get('year')
    if year:
        movies = movies.filter(year=year)
    
    # Get all categories for filter (filtered by language)
    categories = MovieCategory.objects.filter(language=current_language)
    
    # Pagination
    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'rating': rating,
        'year': year,
        'category': category,
        'categories': categories,
    }
    return render(request, 'reviews/movie_list.html', context)


def movie_detail(request, slug):
    """Movie review detail page"""
    current_language = request.LANGUAGE_CODE
    movie = get_object_or_404(MovieReview.objects.select_related('author'), slug=slug, is_published=True, language=current_language)
    
    # Increment views
    movie.increment_views()
    
    # Get related movies
    related_movies = MovieReview.objects.filter(
        is_published=True,
        language=current_language
    ).exclude(id=movie.id).select_related('author')[:3]
    
    # Get comments
    movie_content_type = ContentType.objects.get_for_model(MovieReview)
    comments = Comment.objects.filter(
        content_type=movie_content_type,
        object_id=movie.id,
        is_approved=True,
        parent__isnull=True
    ).select_related('user').prefetch_related('replies')
    
    # Handle comment form
    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_type = ContentType.objects.get_for_model(MovieReview)
            comment.object_id = movie.id
            if request.user.is_authenticated:
                comment.user = request.user
                comment.name = request.user.get_full_name() or request.user.username
                comment.email = request.user.email
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting moderation.')
            return redirect('reviews:movie_detail', slug=slug)
    else:
        form = CommentForm(user=request.user)
    
    context = {
        'movie': movie,
        'related_movies': related_movies,
        'comments': comments,
        'form': form,
    }
    return render(request, 'reviews/movie_detail.html', context)


def book_category_detail(request, slug):
    """Book category detail page"""
    current_language = request.LANGUAGE_CODE
    category = get_object_or_404(BookCategory, slug=slug, language=current_language)
    books = BookReview.objects.filter(is_published=True, category=category, language=current_language).select_related('author', 'category')
    
    # Pagination
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'reviews/book_category_detail.html', context)


def movie_category_detail(request, slug):
    """Movie category detail page"""
    current_language = request.LANGUAGE_CODE
    category = get_object_or_404(MovieCategory, slug=slug, language=current_language)
    movies = MovieReview.objects.filter(is_published=True, category=category, language=current_language).select_related('author', 'category')
    
    # Pagination
    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'reviews/movie_category_detail.html', context)
