from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from ..decorators import allowed_users, app_available

@app_available
@login_required
@allowed_users(['admin'])
def views(request):
    app = db.App.objects.all().first()
    admin = db.Admin.objects.get(user__username=request.user)
    
    candidate_q = db.Candidate.objects.all()

    context = {
        "app": app,
        "admin": admin,
        "tot_division": db.Division.objects.all().count(),
        "tot_voter": db.Voter.objects.all().count(),
        "tot_candidate": candidate_q.count(),
        "tot_voted": db.Voice.objects.all().count(),
    }
    return render(request, "dashboard.html", context)

def get_candidates(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "GET":
            candidates = []
    
            for c in db.Candidate.objects.all():
                candidates.append({
                    "name": c.name,
                    "voice": c.get_voice
                })
            
            result['status'] = True
            result['data'] = candidates
    return JsonResponse(result)

@login_required
@allowed_users(['admin'])
def get_voters(request):
    result = { "status": False }
    
    if request.is_ajax():
        if request.method == "GET":
            voters = [
                {
                    "name": "Total Sudah Voting",
                    "total": db.Voice.objects.all().count()
                },
                {
                    "name": "Total Belum Voting",
                    "total": db.Voter.objects.all().count() - db.Voice.objects.all().count()
                }
            ]
            
            result['status'] = True
            result['data'] = voters
    return JsonResponse(result)