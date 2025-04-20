from django.contrib.auth.backends import ModelBackend

from storefront.models import StoreCustomerUser


# class StoreCustomerBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         if not hasattr(request, 'store'):
#             return None
#         try:
#             user = StoreCustomerUser.objects.get(email=username, store=request.store)
#             if user.check_password(password):
#                 return user
#         except StoreCustomerUser.DoesNotExist:
#             return None


class StoreCustomerBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not hasattr(request, 'store'):
            return None
        try:
            user = StoreCustomerUser.objects.get(email=username, store=request.store)
            if user.check_password(password):
                return user
        except StoreCustomerUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return StoreCustomerUser.objects.get(pk=user_id)
        except StoreCustomerUser.DoesNotExist:
            return None