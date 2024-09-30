from django.urls import path
from . import views

urlpatterns = [
    path('parse_file', views.parse_file), 
]
