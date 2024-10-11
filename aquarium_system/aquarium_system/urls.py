from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from aquarium.views import home_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('aquarium.urls')),
    path('', home_view, name='home'),    
]