from django.urls import path
from . import views

app_name = 'logs'  # Define the namespace

urlpatterns = [
    path('', views.index, name='index'),
]
