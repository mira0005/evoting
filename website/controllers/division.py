from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.contrib.auth.models import User
from random import randint
from tablib import Dataset
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
    return render(request, "division.html", context)

@login_required
@allowed_users(['admin'])
def get_divisions(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "GET":
            divisions = []
            
            data = db.Division.objects.all()
            for d in data:
                divisions.append({
                    "id": d.id,
                    "code": d.code,
                    "name": d.name,
                    "t_voters": '<span class="badge badge-primary">'+str(d.get_voters)+'</span>'
                })
            
            result['data'] = divisions
    return JsonResponse(result)

@login_required
@allowed_users(['admin'])
def add(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "POST":
            name = request.POST.get('name')
            code = request.POST.get('code')
            
            if name:
                try:
                    division = db.Division(name=name, code=code)
                    division.save()
                    
                    result['status'] = True
                except:
                    result['message'] = "Tambah data divisi gagal, coba lagi!"
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
            idd = request.POST.get('id')
            code = request.POST.get('code')
            
            if name:
                try:
                    division = db.Division.objects.get(id=idd)
                    division.name = name
                    division.code = code
                    division.save()
                    
                    result['status'] = True
                except:
                    result['message'] = "Ubah data divisi gagal, coba lagi!"
            else:
                result['message'] = "Ada form yang masih kosong!"
                    
    return JsonResponse(result)

@login_required
@allowed_users(['admin'])
def delete(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "POST":
            idd = request.POST.get('id')
            
            try:
                division = db.Division.objects.get(id=idd)
                division.delete()
                
                result['status'] = True
            except:
                result['message'] = "Hapus data divisi gagal, coba lagi!"
                    
    return JsonResponse(result)

@login_required
@allowed_users(['admin'])
def imports(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "POST":
            dataset = Dataset()
            data_voters = request.FILES.get('file')
            
            if not data_voters.name.endswith('.xlsx'):
                result['message'] = 'File harus berformat ".xlsx"'
            else:
                imported_data = dataset.load(data_voters.read(), format='xlsx')
                error = {}
                error_null = 0
                error_code = 0
                
                for data in imported_data:
                    if data[1] and data[2]:
                        check = db.Division.objects.filter(code=data[2])
                        
                        if not check:
                            division = db.Division(code=data[2], name=data[1])
                            division.save()
                                
                            result['status'] = True
                        else:
                            error_code += 1
                    else:
                        error_null += 1
                        
                error["error_null"] = error_null
                error["error_code"] = error_code
                
                result["error"] = error
                        
    return JsonResponse(result, safe=False)                        