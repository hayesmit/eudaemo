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
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('single_meal', views.single_meal, name='single_meal'),
    path('google_meal', views.google_meal, name='google_meal'),
    path('single_workout', views.single_workout, name='single_workout'),
    path('google_workout', views.google_workout, name='google_workout'),
    path('google_book', views.google_book, name='google_book'),
]
