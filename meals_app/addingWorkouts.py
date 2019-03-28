from django.shortcuts import render
from .models import Workout
import requests
from bs4 import BeautifulSoup
import json

'https://cookieandkate.com/?s=quinoa'


def add_meal(name, shoppingList, ingredients, instructions, prepTime, cookTime, totalTime, servings):
    new_meal = Recipe(name=name, shopping_list=shoppingList, ingredients=ingredients, instructions=instructions, prep_time=prepTime, cook_time=cookTime, total_time=totalTime, servings=servings)
    new_meal.save()


def add_meals(recipesUrl):
    source = requests.get(recipesUrl).text

    soup = BeautifulSoup(source, "html.parser")

    for article in soup.findAll('article'):
        #get next url
        url = article.find('a')
        #get title of the dish to make
        title = url.text
        print(title)
        if title == '':
            continue

        url_href = url['href']
        #print(url['href'])
        open_link = requests.get(url_href).text
        new_page = BeautifulSoup(open_link, "html.parser")
        #print(new_page.prettify())
        correctHeading = new_page.findAll('script', type='application/ld+json')
        recipeInformation = json.loads(correctHeading[1].text)
        ingredients = ', '.join(recipeInformation['recipeIngredient'])
        prepTime = new_page.find(class_='tasty-recipes-prep-time').text
        cookTime = new_page.find(class_='tasty-recipes-cook-time').text
        totalTime = new_page.find(class_='tasty-recipes-total-time').text
        servings = new_page.find(class_='tasty-recipes-yield').text
        # print("prep time: " + prepTime)
        # print('cook time: ' + cookTime)
        # print('total time: ' + totalTime)
        # print('servings: ' + servings)
        # print(ingredients)
        instructions = ', '.join(recipeInformation['recipeInstructions'])
        # print(instructions)
        shorten = ingredients.split(", ")
        # any ingredient that we might need to get from the store is going to start with one of the units in this list, add more as needed.
        units = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "1/4", "1/3", "1/2", "teaspoon", "Freshly", "teaspoons", "tablespoon", "tablespoons", "Pinch", "cup", "cups", 'Scant', "(15 ounces)", "(32 ounces)", "(28 ounces)"]
        # shopping_list is the list of all the items and the quantity of those items that you are going to need to prepare the meal.
        shopping_list = []
        # putting new item on shopping list
        for item in shorten:
            # print(item)
            # split up each word in the list of items so that we can single out the first word or number in the item.
            i = item.split(" ")
            # print(i)
            # checking first word
            if i[0] in units:
                if len(shopping_list) > 0:
                    shopping_list.extend(', ' + item)
                else:
                    shopping_list.extend(item)
        shopping_list = ''.join(shopping_list)
        print(shopping_list)
        add_meal(name=title, shoppingList=shopping_list, ingredients=ingredients, instructions=instructions, prepTime=prepTime, cookTime=cookTime, totalTime=totalTime, servings=servings)
