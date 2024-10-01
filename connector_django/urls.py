"""
URL configuration for connector_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from instruments import views as inst_views
from logs import views as logs_views

urlpatterns = [
    path('', include('mainapp.urls')),
    path('admin/', admin.site.urls),
    path('instruments/', include('instruments.urls')),
    path('logs/', logs_views.index),
    path('connectors/', include('connectors.urls')),
    path('testapp/', include('testapp.urls'))
]
