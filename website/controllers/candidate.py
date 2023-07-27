from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.contrib.auth.models import User
from random import randint
from tablib import Dataset
import uuid
from ..decorators import allowed_users, app_available

@app_available
@login_required
@allowed_users(['admin'])
def views(request):
    app = db.App.objects.all().first()
    admin = db.Admin.objects.get(user__username=request.user)
    division = db.Division.objects.all()
    candidates = db.Candidate.objects.all()
    
    context = {
        "app": app,
        "admin": admin,
        "division": division,
        "candidates": candidates
    }
    return render(request, "candidate.html", context)

@login_required
@allowed_users(['admin'])
def add(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "POST":
            name = request.POST.get('name')
            division = request.POST.get('division')
            order = request.POST.get('order')
            foto = request.FILES.get('foto')
            vision = request.POST.get('vision')
            mission = request.POST.get('mission')
            
            if name and foto and mission and division and vision and order:
                try:
                    candidate = db.Candidate(
                        code=uuid.uuid4().hex[:8],
                        name=name, 
                        order=order, 
                        division=db.Division.objects.get(id=division),
                        photo=foto,
                        vision=vision, 
                        mission=mission, 
                    )
                    candidate.save()
                    
                    result['status'] = True
                except:
                    result['message'] = "Tambah data kandidat gagal, coba lagi!"
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
            division = request.POST.get('division')
            order = request.POST.get('order')
            foto = request.FILES.get('foto')
            vision = request.POST.get('vision')
            mission = request.POST.get('mission')
            code = request.POST['code']
            
            if name and mission and division and vision and order:
                try:
                    candidate = db.Candidate.objects.get(code=code)
                    candidate.name = name
                    candidate.order = order
                    candidate.division = db.Division.objects.get(id=division)
                    
                    if foto:
                        candidate.photo = foto
                        
                    candidate.vision = vision
                    candidate.mission = mission
                    candidate.save()
                    
                    result['status'] = True
                except:
                    result['message'] = "Ubah data kandidat gagal, coba lagi!"
            else:
                result['message'] = "Ada form yang masih kosong!"
                    
    return JsonResponse(result)

@login_required
@allowed_users(['admin'])
def views_update(request, code):
    app = db.App.objects.all().first()
    admin = db.Admin.objects.get(user__username=request.user)
    division = db.Division.objects.all()
    candidates = db.Candidate.objects.get(code=code)
    
    context = {
        "app": app,
        "admin": admin,
        "division": division,
        "c": candidates
    }
    return render(request, 'candidate-update.html', context)

@login_required
@allowed_users(['admin'])
def delete(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "POST":
            code = request.POST.get('code')
            
            try:
                candidate = db.Candidate.objects.get(code=code)
                candidate.delete()
                
                result['status'] = True
            except:
                result['message'] = "Hapus data kandidat gagal, coba lagi!"
                    
    return JsonResponse(result)                     