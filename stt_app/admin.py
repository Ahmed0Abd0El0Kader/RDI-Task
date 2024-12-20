from django.contrib import admin
from .models import AudioFile, UserQuota

# Register your models here.

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'duration', 'uploaded_at')

@admin.register(UserQuota)
class UserQuotaAdmin(admin.ModelAdmin):
    list_display = ('user', 'quota_minutes', 'used_minutes')