"""
Custom URL path converters for Parsa Journal
Supports Unicode characters including Persian/Farsi
"""
from django.urls.converters import StringConverter


class UnicodeSlugConverter(StringConverter):
    """
    A slug converter that accepts Unicode characters including Persian/Farsi.
    Matches any non-empty string containing Unicode word characters, hyphens, and underscores.
    In Python 3, \w already includes Unicode word characters, so this should work for Persian.
    """
    regex = r'[-\w]+'  # This includes Unicode word chars in Python 3


