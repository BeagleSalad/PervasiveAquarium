from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Aquarium, Thermostat, TemperatureLog
from .serializers import AquariumSerializer, ThermostatSerializer, TemperatureLogSerializer
from rest_framework import generics
from .models import Aquarium
from .serializers import AquariumSerializer, ThermostatSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from .serializers import AquariumSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes





def home_view(request):
    return HttpResponse("<h1>Welcome to the Aquarium API</h1><p>Use /api/ to access the API.</p>")

# ViewSets for CRUD operations
class AquariumViewSet(viewsets.ModelViewSet):
    queryset = Aquarium.objects.all()
    serializer_class = AquariumSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Aquarium.objects.filter(owner=self.request.user)

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ThermostatViewSet(viewsets.ModelViewSet):
    queryset = Thermostat.objects.all()
    serializer_class = ThermostatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter thermostats by aquariums owned by the logged-in user
        return Thermostat.objects.filter(aquarium__owner=self.request.user)

class TemperatureLogViewSet(viewsets.ModelViewSet):
    queryset = TemperatureLog.objects.all()
    serializer_class = TemperatureLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter temperature logs by thermostats owned by the user's aquariums
        return TemperatureLog.objects.filter(thermostat__aquarium__owner=self.request.user)
    
class CustomLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this
def user_details(request):
    """
    Returns the authenticated user's details.
    """
    user = request.user  # The logged-in user making the request
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })