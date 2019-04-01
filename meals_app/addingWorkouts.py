from django.shortcuts import render
from .models import Workout
import requests
from bs4 import BeautifulSoup
import json

'https://cookieandkate.com/?s=quinoa'


# def add_meal(name, shoppingList, ingredients, instructions, prepTime, cookTime, totalTime, servings):
#     new_meal = Recipe(name=name, shopping_list=shoppingList, ingredients=ingredients, instructions=instructions, prep_time=prepTime, cook_time=cookTime, total_time=totalTime, servings=servings)
#     new_meal.save()

def add_workout(workout):
    new_workout = Workout(workout=workout)
    new_workout.save()


def add_workouts(workoutUrl):
    url = workoutUrl
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # print(url)
    # print(soup)
    # print(soup.findAll('div'))
    source = requests.get(workoutUrl, headers=headers).text
    soup = BeautifulSoup(source, "html.parser")
    ultag = soup.find('ul', {'class': ['workout-list']})
    # print(workout.prettify())
    this_workout = []
    for litag in ultag.find_all('li'):
        this_workout.append(litag.text)
        # print(litag.text)
    this_workout = ' ,'.join(this_workout)
    add_workout(this_workout)
    print(this_workout + " has been added to DB")
    # this_workout = workout.text()
    # print(this_workout)
    # page = page + 1
#
#
# 'AMRAP in 7 minutes, 3 Thrusters (100/65 lb), 3 Chest-to-Bar Pull-Ups, 6 Thrusters (100/65 lb), 6 Chest-to-Bar Pull-Ups, 9 Thrusters (100/65 lb), 9 Chest-to-Bar Pull-Ups, If you complete the round of 9, complete a round of 12, then go on to 15, etc.'
# python manage.py shell
# from meals_app import addingWorkouts
# addingWorkouts.add_workouts('https://wodwell.com/wod/open-11-/')
