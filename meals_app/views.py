from django.shortcuts import render
from django.http import JsonResponse
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from oauth2client import file, client
from datetime import datetime, timedelta
import random
from .models import Recipe
from django.shortcuts import get_object_or_404


# @login_required
def home(request):
    return render(request, 'core/home.html')


@login_required
def add_meal(request):
    random_meal = random.randint(1, 18)
    meal_details = get_object_or_404(Recipe, pk=random_meal)
    print(meal_details.name)
    # print(meal_details['shopping_list'])
    query = request.POST
    print(query)
    print((query['calDate']))
    time = query['calTime'].split(':')
    time[0] = str(int(time[0])+1)
    # print('time changed to')
    # print(time)
    social = request.user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']
    credentials = client.AccessTokenCredentials(access_token, 'eudaemo')
    GMT_OFF = '-07:00'
    EVENT = {
        'summary': meal_details.name,
        'start': {'dateTime': str(query['calDate'])+'T' + query['calTime'] + ':00%s' % GMT_OFF},
        'end': {'dateTime': str(query['calDate'])+'T' + time[0] + ':' + time[1] + ':00%s' % GMT_OFF},
        'description': meal_details.ingredients + '\n \n' + meal_details.instructions
    }

    service = build('calendar', 'v3', credentials=credentials)
    event = service.events().insert(calendarId='primary', body=EVENT).execute()
    print(event)
    return render(request, 'core/home.html')
    # return JsonResponse({"access_token": social.extra_data['access_token']})


