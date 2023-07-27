from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from ..decorators import allowed_users, app_available

@app_available
def views(request):
    app = db.App.objects.all().first()
    return render(request, "grafik.html", {"app": app})