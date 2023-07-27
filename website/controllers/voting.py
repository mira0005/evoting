from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from ..decorators import allowed_users, app_available
from django.contrib.auth import logout
import datetime

@app_available
def views(request):
    app = db.App.objects.all().first()
    voter = "Votters"
    if request.user.is_authenticated:
        voter = db.Voter.objects.get(user__username=request.user)
    candidates = db.Candidate.objects.all()
    
    return render(request, "voting.html", {
        "app": app, 
        "voter": voter,
        "candidates": candidates
    })
    
@login_required
@allowed_users(['voter'])
def vote(request):
    result = { "status": False }
            
    code = request.POST.get('code')
    
    app = db.App.objects.all().first()
    
    if code:
        if (datetime.datetime.now().timestamp() > app.start_at.timestamp()) and (datetime.datetime.now().timestamp() < app.end_at.timestamp()):
            can = db.Candidate.objects.filter(code=code)
            if can.exists():
                voter = db.Voter.objects.get(auth=request.user)
                if not voter.is_vote:
                    try:
                        vote = db.Voice(voter=voter, candidate=can[0])
                        vote.save()
                        
                        voter.is_vote = True
                        voter.save()
                        
                        logout(request)
                        
                        result['status'] = True
                    except:
                        result['message'] = "Voting gagal, coba lagi nanti!"
                else:
                    logout(request)
                    result['message'] = "Anda sudah melakukan Voting!"
            else:
                result['message'] = "Kandidat terpilih tidak ada!"
        elif datetime.datetime.now().timestamp() > app.end_at.timestamp():
            result['message'] = "Voting telah selesai!"
        else:
            result['message'] = "Voting belum dimulai, mohon tunggu!"
    else:
        result['message'] = "Kode kandidat tidak valid!"
    
    return JsonResponse(result)