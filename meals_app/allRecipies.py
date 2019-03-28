from django.shortcuts import render
from .models import Recipe
import requests
from bs4 import BeautifulSoup
import json


def add_meal(name, shoppingList, ingredients, instructions, prepTime, cookTime, totalTime, servings):
    new_meal = Recipe(name=name, shopping_list=shoppingList, ingredients=ingredients, instructions=instructions, prep_time=prepTime, cook_time=cookTime, total_time=totalTime, servings=servings)
    new_meal.save()


'https://cookieandkate.com/?s=quinoa'
# allRecipies.add_meals('https://cookieandkate.com/category/food-recipes/entrees/page/2/')


def add_meals(recipesUrl, num):
    for this in range(10):
        source = requests.get(recipesUrl + num).text

        soup = BeautifulSoup(source, "html.parser")

        # lcp_catlist_item was article
        # each was article
        for each in soup.findAll('div', {'class': 'lcp_catlist_item'}):
            #get next url
            url = each.find('a')
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
            requires_cooking = new_page.find(class_='tasty-recipes-cook-time')
            cookTime = new_page.find(class_='tasty-recipes-cook-time').text if requires_cooking else 'No cooking required'
            totalTime = new_page.find(class_='tasty-recipes-total-time').text
            has_servings = new_page.find(class_='tasty-recipes-yield')
            servings = new_page.find(class_='tasty-recipes-yield').text if has_servings else 'Servings not indicated'
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
            # print(ingredients)
            # print(type(title))
            # print(type(shopping_list))
            # print(type(ingredients))
            # print(type(instructions))
            # print(type(prepTime))
            # print(type(cookTime))
            # print(type(totalTime))
            # print(type(servings))
            add_meal(name=title, shoppingList=shopping_list, ingredients=ingredients, instructions=instructions, prepTime=prepTime, cookTime=cookTime, totalTime=totalTime, servings=servings)
        num = list(num)
        if int(num[0]) == 1 and num[1] != '/':
            num = str(num[0]) + str(int(num[1])+1) + '/'
        else:
            num = int(num[0])+1
            num = str(num)+'/'
