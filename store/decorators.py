from django.contrib.auth.decorators import user_passes_test
from store_admin.models import StoreOwnerUser

def store_owner_required(view_func):
    return user_passes_test(lambda u: isinstance(u, StoreOwnerUser),
                            login_url='/manage/login')(view_func)