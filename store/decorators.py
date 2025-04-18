# store/decorators.py
from django.contrib.auth.decorators import user_passes_test

def store_owner_required(view_func):
    return user_passes_test(lambda u: hasattr(u, 'storeowneruser'))(view_func)
