from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from aquarium.views import home_view 
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),    
]