from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AquariumViewSet, ThermostatViewSet, TemperatureLogViewSet, CustomLoginView
from rest_framework.authtoken.views import obtain_auth_token  # For token authentication
from aquarium.views import user_details
from django.contrib.auth import views as auth_views

# Create a router and register your viewsets
router = DefaultRouter()
router.register(r'aquariums', AquariumViewSet)
router.register(r'thermostats', ThermostatViewSet)
router.register(r'temperature-logs', TemperatureLogViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include the router's URLs
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Endpoint to obtain auth token
    path('api/', include(router.urls)),
    path('api/user-details/', user_details, name='user_details'),
    path('api/login/', CustomLoginView.as_view(), name='custom_login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
