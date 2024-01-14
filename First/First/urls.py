"""
URL configuration for First project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from hello import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.index, name='login'),
    path('admin/', admin.site.urls),
    path('registration/', views.registration, name='registration'),
    path('test/', views.test, name='test'),
    # path('admin/', views.admin, name='admin')

]

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'AvitoParser'

