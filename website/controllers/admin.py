from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.contrib.auth.models import User
from random import randint
from tablib import Dataset
from django.contrib.auth.hashers import make_password
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
    return render(request, "admin.html", context)

@login_required
@allowed_users(['admin'])
def get_admins(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "GET":
            admins = []
            
            data = db.Admin.objects.all()
            for d in data:
                admins.append({
                    "id": d.id,
                    "name": d.name,
                    "username": d.user.username,
                })
            
            result['data'] = admins
    return JsonResponse(result)

@login_required
@allowed_users(['admin'])
def add(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "POST":
            name = request.POST.get('name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if name and username and password:
                try:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    
                    admin = db.Admin(user=user, name=name)
                    admin.save()
                    
                    result['status'] = True
                except:
                    result['message'] = "Tambah data admin gagal, coba lagi!"
            else:
                result['message'] = "Ada form yang masih kosong!"
                    
    return JsonResponse(result)

@login_required
@allowed_users(['admin'])
def update(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "POST":
            name = request.POST.get('name')
            ids = request.POST.get('id')
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if name and username:
                try:
                    admin = db.Admin.objects.get(id=ids)
                    admin.name = name
                    admin.save()
                    
                    user = User.objects.get(id=admin.user.id)
                    user.username = username
                    
                    if password:
                        user.password = make_password(password, hasher="pbkdf2_sha256")
                    
                    user.save()
                    
                    result['status'] = True
                except:
                    result['message'] = "Ubah data admin gagal, coba lagi!"
            else:
                result['message'] = "Ada form yang masih kosong!"
                    
    return JsonResponse(result)

@login_required
@allowed_users(['admin'])
def delete(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "POST":
            ids = request.POST.get('id')
            
            try:
                admin = User.objects.get(id=db.Admin.objects.get(id=ids).user.id)
                admin.delete()
                
                result['status'] = True
            except:
                result['message'] = "Hapus data admin gagal, coba lagi!"
                    
    return JsonResponse(result)