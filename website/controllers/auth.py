from django.shortcuts import render, redirect
from django.http import JsonResponse
from .. import models as db
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users, app_available
import datetime

def views_install(request):
    if db.App.objects.all().exists():
        return redirect('login')
    else:
        return render(request, "install.html")
    
def install_handle(request):
    result = { "status": False }
    
    app = db.App.objects.all()
    if not app.exists():
        if request.is_ajax():
            logo = request.FILES.get('logo')
            name = request.POST.get('name')
            org = request.POST.get('org')
            adminName = request.POST.get('adminName')
            username = request.POST.get('username')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            
            if logo and name and org and adminName and username and password and password2:
                if password2 == password:
                    apps = db.App(app_name=name, organization=org, app_logo=logo)
                    apps.save()
                    
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    
                    admin = db.Admin(user=user, name=adminName)
                    admin.save()
                    
                    result['status'] = True
                else:
                    result['message'] = "Konfirmasi password tidak sama!"
            else:
                    result['message'] = "Ada form yang masih kosong!"
    else:
        return redirect("login")
                    
    return JsonResponse(result)

@app_available
def views(request):
    app = db.App.objects.all().first()
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, "login.html", {"app": app})
    else:
        result = { "status": False }
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            checku = User.objects.filter(username=username)
            if checku.exists():
                checkp = check_password(password, checku[0].password)
                if checkp:
                    login(request, checku[0])
                    result['status'] = True
                else:
                    result['message'] = "Passwordmu salah!"
            else:
                result['message'] = "Usernamemu tidak diketahui!"
        
        return JsonResponse(result)
    
def voter_login(request):
    result = { "status": False }
            
    kode = request.POST.get('kode')
    kode2 = request.POST.get('kode2')
    
    app = db.App.objects.all().first()
    
    if kode and kode2:
        if (datetime.datetime.now().timestamp() > app.start_at.timestamp()) and (datetime.datetime.now().timestamp() < app.end_at.timestamp()):
            if not db.Voice.objects.filter(voter__auth=kode).exists():
                checku = User.objects.filter(username=kode)
                if kode2 == kode:
                    if checku.exists():
                        checkp = check_password(kode, checku[0].password)
                        if checkp:
                            login(request, checku[0])
                            result['status'] = True
                        else:
                            result['message'] = "Kode salah!"
                    else:
                        result['message'] = "kode tidak diketahui!"
                else:
                    result['message'] = "Konfirmasi kode tidak sama!"
            else:
                result['message'] = "Anda sudah melakukan Voting!"
        elif datetime.datetime.now().timestamp() > app.end_at.timestamp():
            result['message'] = "Voting telah selesai!"
        else:
            result['message'] = "Voting belum dimulai, mohon tunggu!"
    
    return JsonResponse(result)

@login_required(login_url='/')
def voter_logout(request):
    logout(request)
    return redirect('home')
    
@login_required(login_url='/adm/auth/login/')
def logouts(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('dashboard')
        