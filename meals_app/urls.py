from django.urls import path
from . import views

app_name = "meals_app"

urlpatterns = [
    path('', views.home, name='home'),
    path('add_meal', views.add_meal, name='add_meal'),
    path('one_day', views.one_day, name='one_day'),
]
# posibly need to add asView to the end of views
