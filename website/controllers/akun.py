from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from ..decorators import allowed_users, app_available
from django.contrib.auth import logout

@app_available
def views(request):
    app = db.App.objects.all().first()
    voter = "Votters"
    if request.user.is_authenticated:
        voter = db.Voter.objects.get(user__username=request.user)
    
    return render(request, "akun.html", {
        "app": app, 
        "voter": voter,
    })