from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=20, default="admin")
    
    def __str__(self):
        return self.name
    
class Division(models.Model):
    code = models.CharField(max_length=4, null=True)
    name = models.CharField(max_length=255)
    
    @property
    def get_voters(self):
        return Voter.objects.filter(division=self).count()
    
    def __str__(self):
        return self.name
    
class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True)
    level = models.CharField(max_length=20, default="voter")
    auth = models.CharField(max_length=10, null=True)
    is_vote = models.BooleanField(default=False)
    
    def __str__(self):
            return self.name
        
    @property
    def get_voice(self):
        return Voice.objects.filter(voter=self)

class App(models.Model):
    app_name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    app_logo = models.ImageField(upload_to="logo")
    start_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    end_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    
    def __str__(self):
        return self.app_name
    
    @property
    def check_date(self):
        import datetime
        
        if (round(datetime.datetime.now().timestamp()) + 1) < round(self.start_at.timestamp()):
            return "belum"
        elif ((round(datetime.datetime.now().timestamp()) + 1) >= round(self.start_at.timestamp())) and ((round(datetime.datetime.now().timestamp()) + 1) < round(self.end_at.timestamp())):
            return "mulai"
        else:
            return "selesai"
            
    
@receiver(pre_save, sender=App)
def logo_app_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_file = App.objects.get(pk=instance.pk).app_logo
        except App.DoesNotExist:
            return False
        else:
            new_file = instance.app_logo
            if old_file and old_file.url != new_file.url:
                old_file.delete(save=False)

@receiver(post_delete, sender=App)
def logo_app_delete(sender, **kwargs):
    filed = kwargs['instance']
    if filed.app_logo:
        storage, path = filed.app_logo.storage, filed.app_logo.path
        storage.delete(path)
    
class Candidate(models.Model):
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    photo = models.ImageField(upload_to="photos")
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True)
    vision = models.TextField()
    mission = models.TextField()
    
    class Meta:
        ordering = ['order']
    
    @property
    def get_voice(self):
        return Voice.objects.filter(candidate=self).count()
    
    def __str__(self):
        return self.name
    
@receiver(pre_save, sender=Candidate)
def photo_candidate_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_file = Candidate.objects.get(pk=instance.pk).photo
        except Candidate.DoesNotExist:
            return False
        else:
            new_file = instance.photo
            if old_file and old_file.url != new_file.url:
                old_file.delete(save=False)

@receiver(post_delete, sender=Candidate)
def photo_candidate_delete(sender, **kwargs):
    filed = kwargs['instance']
    if filed.photo:
        storage, path = filed.photo.storage, filed.photo.path
        storage.delete(path)
    
class Voice(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    vote_at = models.DateTimeField(auto_now_add=True, null=True)