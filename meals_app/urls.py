from django.urls import path
from . import views

app_name = "meals_app"

urlpatterns = [
    path('', views.home, name='home'),
    path('add_meal', views.add_meal, name='add_meal'),
    path('add_workout', views.add_workout, name='add_workout'),
    path('one_day', views.one_day, name='one_day'),
    path('one_workout', views.one_workout, name='one_workout'),
    path('add_book', views.add_book, name='add_book'),
]
# posibly need to add asView to the end of views
