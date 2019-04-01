from django.shortcuts import render
from django.http import JsonResponse
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from oauth2client import file, client
import datetime
from datetime import datetime, timedelta, date
import random
from .models import Recipe, Workout
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import JsonResponse


def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def single_meal(request):
    return render(request, 'core/singleMeal.html')


def google_meal(request):
    return render(request, 'core/googleMeal.html')


def single_workout(request):
    return render(request, 'core/singleWorkout.html')


def google_workout(request):
    return render(request, 'core/googleWorkout.html')


def google_book(request):
    return render(request, 'core/googleBook.html')


@login_required
def add_meal(request):
    random_meal = random.randint(405, 605)
    meal_details = get_object_or_404(Recipe, pk=random_meal)
    # print(meal_details.name)
    # print(meal_details['shopping_list'])
    query = request.POST
    # print(query)
    print('this is the calDate')
    print((query['calDate']))
    time = query['calTime'].split(':')
    time[0] = str(int(time[0])+1)
    # print('time changed to')
    # print(time)
    # if i decide to add the  shopping list to the previous sunday this will be helpful
    # parsDate = query['calDate']
    # parsDate = parsDate.split('-')
    # print('parsDate is ' + parsDate[0])
    # print(datetime.datetime.today().weekday())
    # print(datetime.datetime(int(parsDate[0]), int(parsDate[1]), int(parsDate[2]), 9, 51, 47, 244794).weekday())
    social = request.user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']
    credentials = client.AccessTokenCredentials(access_token, 'eudaemo')
    GMT_OFF = '-07:00'
    EVENT = {
        'summary': meal_details.name,
        'start': {'dateTime': str(query['calDate'])+'T' + query['calTime'] + ':00%s' % GMT_OFF},
        'end': {'dateTime': str(query['calDate'])+'T' + time[0] + ':' + time[1] + ':00%s' % GMT_OFF},
        'description': 'Shopping List: ' + meal_details.shopping_list + '\n \n' + 'Recipe: ' + meal_details.ingredients + '\n \n' + 'Directions' + meal_details.instructions
    }

    service = build('calendar', 'v3', credentials=credentials)
    event = service.events().insert(calendarId='primary', body=EVENT).execute()
    print(event)
    return render(request, 'core/home.html')
    # return JsonResponse({"access_token": social.extra_data['access_token']})


def one_day(request):
    random_meal = random.randint(405, 605)
    meal_details = get_object_or_404(Recipe, pk=random_meal)
    data = {'cook time': meal_details.cook_time, 'name': meal_details.name, 'shopping_list': meal_details.shopping_list, 'instructions': meal_details.instructions, 'prep_time': meal_details.prep_time, 'servings': meal_details.servings, 'recipe': meal_details.ingredients}
    return JsonResponse(data)


def one_workout(request):
    random_workout = random.randint(1, 62)
    workout_details = get_object_or_404(Workout, pk=random_workout)
    data = {'workout': workout_details.workout}
    return JsonResponse(data)


@login_required
def add_workout(request):
    # if request.user.is_authenticated:
        random_workout = random.randint(1, 62)
        workout_details = get_object_or_404(Workout, pk=random_workout)
        print(workout_details.workout)
        query = request.POST
        # print(query)
        print('this is the calDate')
        print((query['workoutCalDate']))
        time = query['workoutCalTime'].split(':')
        time[0] = str(int(time[0])+1)
        social = request.user.social_auth.get(provider='google-oauth2')
        access_token = social.extra_data['access_token']
        credentials = client.AccessTokenCredentials(access_token, 'eudaemo')
        GMT_OFF = '-07:00'
        EVENT = {
            'summary': "Today's Workout",
            'start': {'dateTime': str(query['workoutCalDate'])+'T' + query['workoutCalTime'] + ':00%s' % GMT_OFF},
            'end': {'dateTime': str(query['workoutCalDate'])+'T' + time[0] + ':' + time[1] + ':00%s' % GMT_OFF},
            'description': 'Workout: ' + workout_details.workout
        }
        service = build('calendar', 'v3', credentials=credentials)
        event = service.events().insert(calendarId='primary', body=EVENT).execute()
        print(event)
        return render(request, 'core/home.html')
    # else:
    #     return render(request, 'registration/login.html')


@login_required
def add_book(request):
    query = request.POST
    title = query['title']
    startDate = query['bookStartDate']
    bookFinishDate = query['bookFinishDate']
    frequency = query['reminderFrequency']
    pages = int(query['pages'])
    start = datetime.strptime(startDate, "%Y-%m-%d")
    # print('start date: ' + str(start))
    # print(start + timedelta(days=1)) to add days to start day
    # print(query['bookFinishDate'])
    finish = datetime.strptime(bookFinishDate, "%Y-%m-%d")
    totalTime = 0
    while start + timedelta(days=totalTime) != finish:
        totalTime += 1
    totalTime += 1
    # print(totalTime)
    PPD = pages/totalTime
    # print(PPD)
    better_date = str(start)
    # print('better date: ' + better_date)
    better_date = better_date.split(' ')
    # print('new better_date: ' + better_date[0])
    start_adding_goals = 0
    while start_adding_goals < totalTime + int(frequency):
        # day_adding_goal = start +timedelta(days=start_adding_goals)
        if start_adding_goals == 0:
            time = query['bookReminderTime'].split(':')
            time[0] = str(int(time[0])+1)
            social = request.user.social_auth.get(provider='google-oauth2')
            access_token = social.extra_data['access_token']
            credentials = client.AccessTokenCredentials(access_token, 'eudaemo')
            GMT_OFF = '-07:00'
            EVENT = {
                'summary': "Start reading " + title,
                'start': {'dateTime': str(query['bookStartDate'])+'T' + query['bookReminderTime'] + ':00%s' % GMT_OFF},
                'end': {'dateTime': str(query['bookStartDate'])+'T' + time[0] + ':' + time[1] + ':00%s' % GMT_OFF},
                'description': 'Today is the day you planned on starting to read the book ' + title + '. Good luck completing it before ' + bookFinishDate + "."
            }
            service = build('calendar', 'v3', credentials=credentials)
            event = service.events().insert(calendarId='primary', body=EVENT).execute()
            print(event)
            start_adding_goals = start_adding_goals + int(frequency)
        elif start_adding_goals >= totalTime:
            time = query['bookReminderTime'].split(':')
            time[0] = str(int(time[0])+1)
            social = request.user.social_auth.get(provider='google-oauth2')
            access_token = social.extra_data['access_token']
            credentials = client.AccessTokenCredentials(access_token, 'eudaemo')
            GMT_OFF = '-07:00'
            EVENT = {
                'summary': title + ' Finished',
                'start': {'dateTime': str(query['bookFinishDate'])+'T' + query['bookReminderTime'] + ':00%s' % GMT_OFF},
                'end': {'dateTime': str(query['bookFinishDate'])+'T' + time[0] + ':' + time[1] + ':00%s' % GMT_OFF},
                'description': 'If you are able to finish ' + title + ' before the end of today you have achieved your goal'
            }
            service = build('calendar', 'v3', credentials=credentials)
            event = service.events().insert(calendarId='primary', body=EVENT).execute()
            print(event)
            return render(request, 'core/home.html')
        elif start_adding_goals < totalTime:
            time = query['bookReminderTime'].split(':')
            time[0] = str(int(time[0])+1)
            page_goal = str(int(round(start_adding_goals * PPD)))
            google_date = start + timedelta(days=start_adding_goals)
            google_date = str(google_date).split(" ")
            google_date = google_date[0]
            print('google date is:' + google_date)
            social = request.user.social_auth.get(provider='google-oauth2')
            access_token = social.extra_data['access_token']
            credentials = client.AccessTokenCredentials(access_token, 'eudaemo')
            GMT_OFF = '-07:00'
            EVENT = {
                'summary': title + ' page: ' + page_goal,
                'start': {'dateTime': google_date+'T' + query['bookReminderTime'] + ':00%s' % GMT_OFF},
                'end': {'dateTime': google_date+'T' + time[0] + ':' + time[1] + ':00%s' % GMT_OFF},
                'description': 'If you are at page ' + page_goal + ' by the end of today, then you are on track for completing ' + title + ' before ' + bookFinishDate + '.'
            }
            service = build('calendar', 'v3', credentials=credentials)
            event = service.events().insert(calendarId='primary', body=EVENT).execute()
            print(event)
            start_adding_goals = start_adding_goals + int(frequency)
    return render(request, 'core/home.html')
