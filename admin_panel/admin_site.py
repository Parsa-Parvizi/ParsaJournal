"""
Custom Admin Site Configuration for Parsa Journal
Secure and personalized admin panel
"""
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class SecureAdminSite(AdminSite):
    """Custom Admin Site with enhanced security"""
    site_header = 'Parsa Journal Administration'
    site_title = 'Parsa Journal Admin'
    index_title = 'Welcome to Parsa Journal Administration'
    
    class Media:
        css = {
            'all': ('admin/css/admin.css',)
        }
        js = ('admin/js/admin.js',)
    
    def has_permission(self, request):
        """
        Only allow superusers and staff members to access admin.
        Optionally restrict by IP address.
        """
        if not request.user.is_active:
            return False
        
        if not request.user.is_staff:
            return False
        
        # Log admin access attempts
        if request.user.is_authenticated:
            logger.info(f"Admin access attempt by {request.user.username} from {self.get_client_ip(request)}")
        
        # Optional: IP whitelist (set in settings)
        from django.conf import settings
        admin_ip_whitelist = getattr(settings, 'ADMIN_IP_WHITELIST', [])
        
        # Filter out empty strings from whitelist
        admin_ip_whitelist = [ip for ip in admin_ip_whitelist if ip]
        
        if admin_ip_whitelist:
            client_ip = self.get_client_ip(request)
            if client_ip not in admin_ip_whitelist and not request.user.is_superuser:
                logger.warning(f"Admin access denied for IP: {client_ip} (not in whitelist)")
                return False
        
        return True
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def login(self, request, extra_context=None):
        """Custom login with security logging"""
        # Log login attempts for POST requests
        if request.method == 'POST':
            username = request.POST.get('username', '')
            client_ip = self.get_client_ip(request)
            logger.info(f"Admin login attempt for username: {username} from IP: {client_ip}")
        
        # Use Django's built-in login handling
        # Django's AdminAuthenticationForm already validates that user is staff
        response = super().login(request, extra_context)
        
        # Log successful login if user is now authenticated
        if request.user.is_authenticated and request.user.is_staff:
            logger.info(f"Successful admin login: {request.user.username} from IP: {self.get_client_ip(request)}")
        
        return response


# Create custom admin site instance
admin_site = SecureAdminSite(name='secure_admin')

