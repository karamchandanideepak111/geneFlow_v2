from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('update/', views.update_connector),
    path('register/', views.register_connector),
    path('delete/', views.delete_connector),
    path('validate', views.validate),
    path('upload', views.upload_file),
]
