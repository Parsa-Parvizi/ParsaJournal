from django import forms
from django.utils.translation import get_language
from .models import Comment


def _is_persian_language() -> bool:
    language = (get_language() or 'en').split('-')[0]
    return language == 'fa'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Email',
                'required': True
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Website (optional)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Your Comment',
                'rows': 5,
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if _is_persian_language():
            placeholders = {
                'name': 'نام شما',
                'email': 'ایمیل شما',
                'website': 'وب‌سایت شما (اختیاری)',
                'content': 'نظر شما',
            }
        else:
            placeholders = {
                'name': 'Your Name',
                'email': 'Your Email',
                'website': 'Your Website (optional)',
                'content': 'Your Comment',
            }
        for field, value in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs['placeholder'] = value
        # If user is authenticated, hide name and email fields (will be filled automatically)
        if self.user and self.user.is_authenticated:
            self.fields['name'].widget = forms.HiddenInput()
            self.fields['email'].widget = forms.HiddenInput()
            self.fields['name'].required = False
            self.fields['email'].required = False
        else:
            # For non-authenticated users, name and email are required
            self.fields['name'].required = True
            self.fields['email'].required = True

