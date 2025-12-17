"""
Admin Panel Forms for Parsa Journal
Custom forms for managing articles and content
"""
from django import forms
from django.utils.text import slugify
from django.utils.translation import get_language
from articles.models import Article, Category, Tag
from accounts.models import Author
from articles.widgets import RichTextareaWidget


def _is_persian_language() -> bool:
    language = (get_language() or 'en').split('-')[0]
    return language == 'fa'


class ArticleForm(forms.ModelForm):
    """Form for creating and editing articles"""
    
    class Meta:
        model = Article
        fields = [
            'title', 'slug', 'author', 'category', 'tags',
            'excerpt', 'content', 'featured_image', 'image_alt',
            'meta_title', 'meta_description',
            'status', 'is_featured', 'published_at'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Article Title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'article-slug-url'
            }),
            'author': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '8',
                'style': 'min-height: 150px;'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Short summary of the article'
            }),
            'content': RichTextareaWidget(attrs={
                'class': 'form-textarea',
                'rows': 20,
                'placeholder': 'Article content'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'image/*'
            }),
            'image_alt': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Image alt text'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'SEO Title (optional)'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2,
                'placeholder': 'SEO Description (optional)'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
            'published_at': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'type': 'datetime-local'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if _is_persian_language():
            placeholders = {
                'title': 'عنوان مقاله',
                'slug': 'اسلاگ مقاله (اختیاری)',
                'excerpt': 'خلاصه‌ای کوتاه از مقاله',
                'content': 'متن مقاله',
                'image_alt': 'متن جایگزین تصویر',
                'meta_title': 'عنوان سئو (اختیاری)',
                'meta_description': 'توضیحات سئو (اختیاری)',
            }
        else:
            placeholders = {
                'title': 'Article Title',
                'slug': 'article-slug-url',
                'excerpt': 'Short summary of the article',
                'content': 'Article content',
                'image_alt': 'Image alt text',
                'meta_title': 'SEO Title (optional)',
                'meta_description': 'SEO Description (optional)',
            }
        for field, value in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs['placeholder'] = value
        # Make slug field optional for auto-generation
        self.fields['slug'].required = False
        # Auto-generate slug from title if not provided
        if 'title' in self.data:
            title = self.data.get('title', '')
            if title and not self.data.get('slug'):
                self.data = self.data.copy()
                self.data['slug'] = slugify(title)
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            # Auto-generate from title
            title = self.cleaned_data.get('title', '')
            if title:
                slug = slugify(title)
            else:
                raise forms.ValidationError('Title is required')
        
        # Check uniqueness
        if self.instance.pk:
            if Article.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('This slug is already in use')
        else:
            if Article.objects.filter(slug=slug).exists():
                raise forms.ValidationError('This slug is already in use')
        
        return slug


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Category Name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'category-slug-url'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Category Description'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'image/*'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if _is_persian_language():
            placeholders = {
                'name': 'نام دسته‌بندی',
                'slug': 'اسلاگ دسته‌بندی (اختیاری)',
                'description': 'توضیحات دسته‌بندی',
            }
        else:
            placeholders = {
                'name': 'Category Name',
                'slug': 'category-slug-url',
                'description': 'Category Description',
            }
        for field, value in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs['placeholder'] = value
        self.fields['slug'].required = False
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            name = self.cleaned_data.get('name', '')
            if name:
                slug = slugify(name)
            else:
                raise forms.ValidationError('Name is required')
        return slug


class TagForm(forms.ModelForm):
    """Form for creating and editing tags"""
    
    class Meta:
        model = Tag
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tag Name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'tag-slug-url'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if _is_persian_language():
            placeholders = {
                'name': 'نام تگ',
                'slug': 'اسلاگ تگ (اختیاری)',
            }
        else:
            placeholders = {
                'name': 'Tag Name',
                'slug': 'tag-slug-url',
            }
        for field, value in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs['placeholder'] = value
        self.fields['slug'].required = False
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            name = self.cleaned_data.get('name', '')
            if name:
                slug = slugify(name)
            else:
                raise forms.ValidationError('Name is required')
        return slug

