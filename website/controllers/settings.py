from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .. import models as db
from ..decorators import allowed_users, app_available

@app_available
@login_required
@allowed_users(['admin'])
def views(request):
    app = db.App.objects.all().first()
    admin = db.Admin.objects.get(user__username=request.user)
    
    context = {
        "app": app,
        "admin": admin,
    }
    return render(request, "settings.html", context)

@login_required
@allowed_users(['admin'])
def update(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "POST":
            name = request.POST.get('name')
            org = request.POST.get('org')
            start = request.POST.get('start')
            end = request.POST.get('end')
            logo = request.FILES.get('logo')
            
            if name and org:
                try:
                    settings = db.App.objects.all().first()
                    settings.app_name = name
                    settings.organization = org
                    
                    if logo:
                        settings.app_logo = logo
                    if start:
                        settings.start_at = start
                    if end:
                        settings.end_at = end
                    settings.save()
                    
                    result['status'] = True
                except:
                    result['message'] = "Ubah pengaturan gagal, coba lagi!"
            else:
                result['message'] = "Ada form yang masih kosong!"
                    
    return JsonResponse(result)                