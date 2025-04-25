from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
import requests, os
from dotenv import load_dotenv
from django.http import JsonResponse
from .models import StravaActivity

# Create your views here.

load_dotenv()
def strava_import(request):
    return render(request, 'strava/strava_import.html')

def strava_login(request):
    client_id = os.getenv('STRAVA_CLIENT_ID')
    redirect_uri = 'http://localhost:8000/strava/callback'
    auth_url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=read,activity:read"
    return redirect(auth_url)

def strava_callback(request):
    code = request.GET.get('code')
    token_url = "https://www.strava.com/oauth/token"
    data = {
        'client_id': os.getenv('STRAVA_CLIENT_ID'),
        'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
        'code': code,
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get('access_token')
    workouts = get_workouts(access_token)
    save_workouts(workouts)
    return redirect('strava.workouts')

def get_workouts(access_token):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    return response.json()

def save_workouts(workouts):
    for activity in workouts:
        StravaActivity.objects.create(
            name=activity['name'],
            activity_type=activity['type'],
            distance=activity['distance'],
            moving_time=activity['moving_time'],
            date=activity['start_date'],
        )

def show_workouts(request):
    workouts = StravaActivity.objects.all()  # Get all imported workouts
    return render(request, 'strava/show_workouts.html', {'workouts': workouts})
