"""
Alternative admin site registration to avoid circular imports
"""
from django.contrib import admin
from config.admin import admin_site

# This file helps with proper admin registration order

