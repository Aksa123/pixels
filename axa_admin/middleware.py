from django.http import request, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, resolve
from datetime import datetime

def admin_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.      

        if (resolve(request.path_info).url_name) != None and "admin" in resolve(request.path_info).url_name:
            if request.user.is_authenticated and request.user.userprofile.role == "admin":
                pass
            else:
                return JsonResponse({
                    "subject": "access denied on branch nanana test2", 
                    "content": "u must be logged in as admin bruh, this is test2", 
                    "by": "Aksa", 
                    "branch": "from test5",
                    "date": datetime.now().strftime("%c")})

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware