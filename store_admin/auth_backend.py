from django.contrib.auth.backends import ModelBackend

from store_admin.models import StoreOwnerUser


class StoreOwnerBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not request or not hasattr(request, 'store'):
            return None  # only authenticate in store context

        try:
            # user = StoreOwnerUser.objects.get(email=username, store=request.store)
            user = StoreOwnerUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except StoreOwnerUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return StoreOwnerUser.objects.get(pk=user_id)
        except StoreOwnerUser.DoesNotExist:
            return None
