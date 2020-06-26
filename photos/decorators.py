from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


def must_login(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("login"))

    return wrapper_func