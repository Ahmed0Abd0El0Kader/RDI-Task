from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AudioFile, UserQuota
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request,'stt_app/index.html')

@login_required
@csrf_exempt
def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            user_quota = UserQuota.objects.get(user=request.user)
        except UserQuota.DoesNotExist:
            return JsonResponse({'error': 'User quota not found'}, status=404)

        # Check if user has exceeded their quota
        if user_quota.used_minutes >= user_quota.quota_minutes:
            return JsonResponse({'error': 'Quota exceeded'}, status=400)

        audio_file = request.FILES['file']

        # TODO: Replace with actual duration calculation (e.g., using pydub)
        duration = 5.0  # Assume 5 seconds for now
        required_minutes = duration / 60
        if user_quota.used_minutes + required_minutes > user_quota.quota_minutes:
            return JsonResponse({'error': 'Not enough quota'}, status=400)

        # Save the audio file to the database
        audio = AudioFile.objects.create(user=request.user, file=audio_file, duration=duration)

        # Call the Kateb API
        url = "https://echo-6sdzv54itq-uc.a.run.app/kateb"
        files = {'file': (audio_file.name, audio_file.file, audio_file.content_type)}
        try:
            response = requests.post(url, files=files)
            if response.status_code == 200:
                transcription = response.json().get('json', {}).get('words', [])
                transcription_text = " ".join([word['text'] for word in transcription])
                audio.transcription = transcription_text
                audio.save()
                return JsonResponse({'transcription': transcription_text})
            else:
                return JsonResponse({
                    'error': f'STT server error: {response.status_code} - {response.text}'
                }, status=500)
           
        except requests.RequestException as e:
            return JsonResponse({'error': f'Service unavailable: {str(e)}'}, status=503)

    return render(request, 'stt_app/index.html')
