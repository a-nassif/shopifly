# store/middleware.py
from django.http import HttpResponseNotFound
from store.models import Store


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Remove port (localhost:8000 → localhost)
        host = request.get_host().split(':')[0]

        # Handle local development
        if host == 'localhost' or host == '127.0.0.1' or host == 'shopifly.local':
            # No subdomain = main platform/landing page
            request.store = None
            request.is_platform = True
            return self.get_response(request)

        # Handle subdomain like store1.localhost
        if host.endswith('.localhost') or host.endswith('.shopifly.local'):
            subdomain = host.split('.')[0]
            try:
                store = Store.objects.get(subdomain=subdomain, is_active=True)
                request.store = store
                request.is_platform = False
            except Store.DoesNotExist:
                return HttpResponseNotFound("Store not found.")
            return self.get_response(request)

        # Handle custom domains like mystore.com
        try:
            store = Store.objects.get(custom_domain=host, is_active=True)
            request.store = store
            request.is_platform = False
        except Store.DoesNotExist:
            # Not a valid store or domain — serve landing page or return 404
            request.store = None
            request.is_platform = True
        return self.get_response(request)
