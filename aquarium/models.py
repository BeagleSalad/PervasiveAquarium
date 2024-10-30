from django.db import models
from django.contrib.auth.models import User

# Aquarium Model: Represents an aquarium owned by a user.
class Aquarium(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to Django's User model
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} (Owner: {self.owner.username})"

# Thermostat Model: Represents a thermostat device for an aquarium.
class Thermostat(models.Model):
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    default_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    aquarium = models.OneToOneField(Aquarium, on_delete=models.CASCADE)  # Each aquarium has one thermostat
    installation_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Thermostat {self.model} (Aquarium: {self.aquarium.name})"

# Temperature Log Model: Stores the temperature history for an aquarium's thermostat.
class TemperatureLog(models.Model):
    thermostat = models.ForeignKey(Thermostat, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.temperature}°C at {self.timestamp} (Thermostat: {self.thermostat.serial_number})"
