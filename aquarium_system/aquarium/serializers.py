from rest_framework import serializers
from .models import Aquarium, Thermostat, TemperatureLog

class AquariumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aquarium
        fields = ['id', 'name', 'location', 'description', 'created_at']

class ThermostatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thermostat
        fields = ['id', 'model', 'serial_number', 'default_temperature', 'installation_date', 'aquarium']

class TemperatureLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureLog
        fields = ['id', 'thermostat', 'temperature', 'timestamp']
