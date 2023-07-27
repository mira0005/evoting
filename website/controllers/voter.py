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
    division = db.Division.objects.all()
    
    context = {
        "app": app,
        "admin": admin,
        "division": division
    }
    return render(request, "voters.html", context)

@login_required
@allowed_users(['admin'])
def get_voters(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "GET":
            voters = []
            
            data = db.Voter.objects.all()
            for d in data:
                vote_at = ''
                if d.get_voice:
                    time = d.get_voice[0].vote_at
                    vote_at = time.strftime("%d %b %Y, %H:%M")+" WIB"
                else:
                    vote_at = '-'
                    
                is_vote = ''
                
                if d.is_vote: 
                    is_vote = '<span class="text-success"><i class="uil uil-check-circle"></i> Selesai</span>'
                else:
                    is_vote = '<span class="text-danger"><i class="uil uil-times-circle"></i> Belum</span>'
                
                voters.append({
                    "name": d.name,
                    "division": d.division.name,
                    "division_id": d.division.id,
                    "auth": d.auth,
                    "vote_at": vote_at,
                    "is_vote": is_vote
                })
            
            result['data'] = voters
    return JsonResponse(result)

@login_required
@allowed_users(['admin'])
def add(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "POST":
            name = request.POST.get('name')
            division = request.POST.get('division')
            auth = ''
            
            for _ in range(10):
                value = randint(0, 9)
                auth += str(value)
            
            if name:
                try:
                    user = User.objects.create_user(username=auth, password=auth)
                    user.save()
                    
                    voter = db.Voter(user=user, name=name, auth=auth, division=db.Division.objects.get(id=division))
                    voter.save()
                    
                    result['status'] = True
                except:
                    result['message'] = "Tambah data pemilih gagal, coba lagi!"
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
            auth = request.POST.get('auth')
            division = request.POST.get('division')
            
            if name:
                try:
                    voter = db.Voter.objects.get(auth=auth)
                    voter.name = name
                    voter.division = db.Division.objects.get(id=division)
                    voter.save()
                    
                    result['status'] = True
                except:
                    result['message'] = "Ubah data pemilih gagal, coba lagi!"
            else:
                result['message'] = "Ada form yang masih kosong!"
                    
    return JsonResponse(result)

@login_required
@allowed_users(['admin'])
def delete(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "POST":
            auth = request.POST.get('auth')
            
            try:
                voter = db.Voter.objects.get(auth=auth)
                user = User.objects.get(id=voter.user.id)
                user.delete()
                
                result['status'] = True
            except:
                result['message'] = "Hapus data pemilih gagal, coba lagi!"
                    
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
                error_division = 0
                for data in imported_data:
                    if data[1] and data[2]:
                        division = db.Division.objects.filter(code=data[2])
                        if division:
                            auth = ''
                            for _ in range(10):
                                value = randint(0, 9)
                                auth += str(value)
                                
                            user = User.objects.create_user(username=auth, password=auth)
                            user.save()
                            
                            voter = db.Voter(user=user, name=data[1], auth=auth, division=division[0])
                            voter.save()
                                
                            result['status'] = True
                        else:
                            error_division += 1
                    else:
                        error_null += 1
                        
                error["error_division"] = error_division
                error["error_null"] = error_null
                
                result["error"] = error
                        
    return JsonResponse(result, safe=False)                        