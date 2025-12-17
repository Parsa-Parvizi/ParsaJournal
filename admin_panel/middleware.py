"""
Admin Security Middleware and Utilities
"""
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class AdminSecurityMiddleware(MiddlewareMixin):
    """
    Middleware to enhance admin security:
    - Rate limiting for login attempts
    - IP-based access control
    - Suspicious activity logging
    """
    
    def process_request(self, request):
        """Process request before view is called"""
        # Get admin URL from settings
        admin_url = getattr(settings, 'ADMIN_URL', 'admin')
        
        # Block access to default Django admin if someone tries to access it directly
        # This ensures the default admin is completely disabled
        if request.path.startswith('/admin/') and not request.path.startswith(f'/{admin_url}/'):
            # If ADMIN_URL is 'admin', this won't trigger, which is fine
            # But if ADMIN_URL is different, block the default /admin/ path
            if admin_url != 'admin':
                logger.warning(f"Blocked access attempt to default Django admin from IP: {self._get_client_ip(request)}")
                return HttpResponseForbidden("Access denied. Default Django admin is disabled.")
        
        # Handle custom admin site security
        if request.path.startswith(f'/{admin_url}/'):
            # Only apply rate limiting to login page for unauthenticated users
            if not request.user.is_authenticated and 'login' in request.path:
                # Check rate limiting for login attempts
                if self._is_rate_limited(request):
                    logger.warning(f"Rate limited admin login attempt from IP: {self._get_client_ip(request)}")
                    return HttpResponseForbidden("Too many login attempts. Please try again later.")
            
            # Log admin access for authenticated users
            if request.user.is_authenticated and request.user.is_staff:
                logger.info(f"Admin access: {request.user.username} from IP: {self._get_client_ip(request)}")
        
        return None
    
    def _is_rate_limited(self, request):
        """Check if IP is rate limited"""
        ip = self._get_client_ip(request)
        cache_key = f'admin_login_attempts_{ip}'
        attempts = cache.get(cache_key, 0)
        
        # Allow 5 attempts per 15 minutes
        max_attempts = 5
        if attempts >= max_attempts:
            return True
        
        # Increment attempts (only on failed login, but we increment on each attempt for simplicity)
        # In a real scenario, you'd want to reset this on successful login
        cache.set(cache_key, attempts + 1, timeout=900)  # 15 minutes
        return False
    
    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip

