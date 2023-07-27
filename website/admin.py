from django.contrib import admin
from . import models as db

admin.site.register(db.App)
admin.site.register(db.Admin)
admin.site.register(db.Voter)
admin.site.register(db.Candidate)
admin.site.register(db.Voice)
admin.site.register(db.Division)