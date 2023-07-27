from django.shortcuts import redirect
from . import models as db
from django.http import HttpResponse
from django.contrib.auth import logout

def allowed_users(roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user = db.Admin.objects.filter(user__username=request.user) or db.Voter.objects.filter(user__username=request.user)
            if user[0].level in roles:
                return view_func(request, *args, **kwargs)
            else:
                logout(request)
                return HttpResponse("Anjay mau ngeheck lu?")
        return wrapper_func
    return decorator

def app_available(view_func):
    def wrapper_func(request, *args, **kwargs):
        app = db.App.objects.all()
        if app.exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('install')
    return wrapper_func