from .models import SiteSettings


def site_info(request):
    """Context processor for site-wide information"""
    try:
        site_settings = SiteSettings.load()
    except:
        site_settings = None
    return {
        'site_settings': site_settings,
    }

