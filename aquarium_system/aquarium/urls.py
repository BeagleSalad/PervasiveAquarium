from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AquariumViewSet, ThermostatViewSet, TemperatureLogViewSet
from rest_framework.authtoken.views import obtain_auth_token  # For token authentication

# Create a router and register your viewsets
router = DefaultRouter()
router.register(r'aquariums', AquariumViewSet)
router.register(r'thermostats', ThermostatViewSet)
router.register(r'temperature-logs', TemperatureLogViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include the router's URLs
    path('api-token-auth/', obtain_auth_token),  # Endpoint to obtain auth token
]
