from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('getinst/', views.instruments_data, name='instruments_data'),
    path('register/', views.create_instrument, name='instruments_data'), 
]
