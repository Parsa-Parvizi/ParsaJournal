"""
Custom widgets for article admin
"""
from django import forms


class RichTextareaWidget(forms.Textarea):
    """Enhanced textarea widget for rich text content"""
    
    class Media:
        css = {
            'all': ('admin/css/richtext.css',)
        }
        js = ('admin/js/richtext.js',)
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'richtext-area',
            'rows': 20,
            'cols': 80,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

