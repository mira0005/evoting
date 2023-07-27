from django.urls import path
from .controllers import dashboard, auth, voter, division, candidate, admin, settings, home, voting, grafik, akun

urlpatterns = [
    path('install-app/', auth.views_install, name='install'),
    path('install-app/install/', auth.install_handle, name='install-handle'),
    path('adm/auth/login/', auth.views, name='login'),
    path('adm/auth/logout/', auth.logouts, name='logout'),
    
    path('adm/dashboard/', dashboard.views, name='dashboard'),
    path('adm/dashboard/get-candidates/', dashboard.get_candidates, name='dashboard-get-candidates'),
    path('adm/dashboard/get-voters/', dashboard.get_voters, name='dashboard-get-voters'),
    
    path('adm/voters/', voter.views, name='voters'),
    path('adm/voters/add/', voter.add, name='voters-add'),
    path('adm/voters/update/', voter.update, name='voters-update'),
    path('adm/voters/delete/', voter.delete, name='voters-delete'),
    path('adm/voters/get-data/', voter.get_voters, name='voters-get'),
    path('adm/voters/import/', voter.imports, name='voters-import'),
    
    path('adm/divisions/', division.views, name='divisions'),
    path('adm/divisions/get-data/', division.get_divisions, name='divisions-get'),
    path('adm/divisions/add/', division.add, name='divisions-add'),
    path('adm/divisions/update/', division.update, name='divisions-update'),
    path('adm/divisions/delete/', division.delete, name='divisions-delete'),
    path('adm/divisions/import/', division.imports, name='divisions-import'),
    
    path('adm/candidates/', candidate.views, name='candidates'),
    path('adm/candidates/add/', candidate.add, name='candidates-add'),
    path('adm/candidates/<str:code>/detail/', candidate.views_update, name='candidates-update-views'),
    path('adm/candidates/update/', candidate.update, name='candidates-update'),
    path('adm/candidates/delete/', candidate.delete, name='candidates-delete'),
    
    path('adm/admins/', admin.views, name='admins'),
    path('adm/admins/get-data/', admin.get_admins, name='admin-get'),
    path('adm/admins/add/', admin.add, name='admin-add'),
    path('adm/admins/update/', admin.update, name='admin-update'),
    path('adm/admins/delete/', admin.delete, name='admin-delete'),
    
    path('adm/settings/', settings.views, name='settings'),
    path('adm/settings/update/', settings.update, name='settings-update'),
    
    # Voters UI
    path('', home.views, name='home'),
    path('auth/login/', auth.voter_login, name='voter-login'),
    path('auth/logout/', auth.voter_logout, name='voter-logout'),
    
    path('voting/', voting.views, name='voting'),
    path('voting/vote/', voting.vote, name='voting-vote'),
    
    path('grafik/', grafik.views, name='grafik'),
    
    path('akun/', akun.views, name='akun'),
    
]
