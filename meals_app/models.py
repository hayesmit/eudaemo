from django.db import models
# from django.contrib.auth.models import User
# from oauth2client.contrib.django_orm import FlowField


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    shopping_list = models.CharField(max_length=100000)
    ingredients = models.CharField(max_length=100000)
    instructions = models.CharField(max_length=100000)
    prep_time = models.CharField(max_length=10)
    cook_time = models.CharField(max_length=10)
    total_time = models.CharField(max_length=10)
    servings = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Workout(models.Model):
    workout = models.CharField(max_length=10000)
