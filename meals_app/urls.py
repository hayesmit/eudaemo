from django.urls import path
from . import views

app_name = "meals_app"

urlpatterns = [
    path('', views.home, name='home'),
    path('add_meal', views.add_meal, name='add_meal'),
]
# posibly need to add asView to the end of views
