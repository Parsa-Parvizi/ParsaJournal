from django import forms
from django.utils.translation import get_language
from .models import ContactMessage


def _is_persian_language() -> bool:
    language = (get_language() or 'en').split('-')[0]
    return language == 'fa'


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
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
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Subject',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Your Message',
                'rows': 6,
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if _is_persian_language():
            placeholders = {
                'name': 'نام شما',
                'email': 'ایمیل شما',
                'subject': 'موضوع پیام',
                'message': 'متن پیام شما',
            }
        else:
            placeholders = {
                'name': 'Your Name',
                'email': 'Your Email',
                'subject': 'Subject',
                'message': 'Your Message',
            }
        for field, value in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs['placeholder'] = value


class NewsletterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email',
            'required': True
        })
    )
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your Name (optional)'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if _is_persian_language():
            self.fields['email'].widget.attrs['placeholder'] = 'ایمیل خود را وارد کنید'
            self.fields['name'].widget.attrs['placeholder'] = 'نام شما (اختیاری)'
        else:
            self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
            self.fields['name'].widget.attrs['placeholder'] = 'Your Name (optional)'

