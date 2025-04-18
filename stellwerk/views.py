from django.shortcuts import render

from storefront.views import store_home


# Create your views here.


def home_dispatcher(request):
    return marketing_landing(request) if request.is_platform else store_home(request)

def marketing_landing(request):
    return render(request, 'stellwerk/index.html')
