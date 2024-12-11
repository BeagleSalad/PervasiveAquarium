from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from aquarium.views import home_view 
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', include('aquarium.urls')),
    path('', home_view, name='home'),    
]
