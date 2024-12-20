from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AudioFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='audio_files/')
    duration = models.FloatField()  # Duration in seconds
    transcription = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class UserQuota(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='quota')
    quota_minutes = models.FloatField(default=60)  # 60 minutes default
    used_minutes = models.FloatField(default=0)

    @classmethod
    def create_quota(cls, sender, instance, created, **kwargs):
        if created:
            cls.objects.create(user=instance)

models.signals.post_save.connect(UserQuota.create_quota, sender=User)
