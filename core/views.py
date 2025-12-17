from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import SiteSettings, ContactMessage
from .forms import ContactForm, NewsletterForm
from articles.models import Article
from reviews.models import BookReview, MovieReview
from newsletter.models import NewsletterSubscriber


def home(request):
    """Home page with latest articles and featured reviews"""
    current_language = request.LANGUAGE_CODE
    # Get latest published articles
    latest_articles = Article.objects.filter(status='published', language=current_language).select_related('author', 'category')[:6]
    
    # Get featured articles
    featured_articles = Article.objects.filter(status='published', is_featured=True, language=current_language).select_related('author', 'category')[:3]
    
    # Get featured reviews
    featured_books = BookReview.objects.filter(is_published=True, is_featured=True, language=current_language).select_related('author', 'category').order_by('-published_at', '-created_at')[:3]
    featured_movies = MovieReview.objects.filter(is_published=True, is_featured=True, language=current_language).select_related('author', 'category').order_by('-published_at', '-created_at')[:3]
    
    # Get latest reviews (excluding featured ones)
    # Convert to list to evaluate queryset and get IDs
    featured_books_list = list(featured_books)
    featured_movies_list = list(featured_movies)
    
    # Get latest books (exclude featured ones if they exist)
    latest_books_query = BookReview.objects.filter(is_published=True, language=current_language).select_related('author', 'category').order_by('-published_at', '-created_at')
    if featured_books_list:
        featured_book_ids = [b.id for b in featured_books_list]
        latest_books = latest_books_query.exclude(id__in=featured_book_ids)[:6]
    else:
        latest_books = latest_books_query[:6]
    
    # Get latest movies (exclude featured ones if they exist)
    latest_movies_query = MovieReview.objects.filter(is_published=True, language=current_language).select_related('author', 'category').order_by('-published_at', '-created_at')
    if featured_movies_list:
        featured_movie_ids = [m.id for m in featured_movies_list]
        latest_movies = latest_movies_query.exclude(id__in=featured_movie_ids)[:6]
    else:
        latest_movies = latest_movies_query[:6]
    
    context = {
        'latest_articles': latest_articles,
        'featured_articles': featured_articles,
        'featured_books': featured_books_list if featured_books_list else [],
        'featured_movies': featured_movies_list if featured_movies_list else [],
        'latest_books': latest_books,
        'latest_movies': latest_movies,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page"""
    site_settings = SiteSettings.load()
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'core/about.html', context)


def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    site_settings = SiteSettings.load()
    context = {
        'form': form,
        'site_settings': site_settings,
    }
    return render(request, 'core/contact.html', context)


def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data.get('name', '')
            
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'name': name, 'is_active': True}
            )
            
            if not created:
                if not subscriber.is_active:
                    subscriber.is_active = True
                    subscriber.unsubscribed_at = None
                    subscriber.save()
                messages.info(request, 'You are already subscribed to our newsletter.')
            else:
                messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))


def search(request):
    """Search functionality for articles and reviews"""
    query = request.GET.get('q', '').strip()
    results = {}
    
    if query:
        # Search articles
        current_language = request.LANGUAGE_CODE
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).filter(status='published', language=current_language).distinct().select_related('author', 'category')
        
        # Search book reviews
        books = BookReview.objects.filter(
            Q(title__icontains=query) |
            Q(book_title__icontains=query) |
            Q(book_author__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query)
        ).filter(is_published=True, language=current_language).distinct().select_related('author')
        
        # Search movie reviews
        movies = MovieReview.objects.filter(
            Q(title__icontains=query) |
            Q(movie_title__icontains=query) |
            Q(director__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query)
        ).filter(is_published=True, language=current_language).distinct().select_related('author')
        
        results = {
            'articles': articles,
            'books': books,
            'movies': movies,
        }
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'core/search.html', context)


def login_view(request):
    """Login page for superuser only - redirects to custom admin panel"""
    
    # If user is already logged in, redirect to custom admin panel
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_panel:dashboard')
        else:
            messages.warning(request, 'You are already logged in, but you need superuser access.')
            return redirect('core:home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
        else:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        # Redirect to custom admin panel
                        return redirect('admin_panel:dashboard')
                else:
                    messages.error(request, 'Access denied. This login is only for superusers.')
            else:
                messages.error(request, 'Invalid username or password.')
    
    site_settings = SiteSettings.load()
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'core/login.html', context)


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('core:home')
