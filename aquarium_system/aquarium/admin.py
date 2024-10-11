from django.contrib import admin
from .models import Aquarium, Thermostat, TemperatureLog

admin.site.register(Aquarium)
admin.site.register(Thermostat)
admin.site.register(TemperatureLog)
