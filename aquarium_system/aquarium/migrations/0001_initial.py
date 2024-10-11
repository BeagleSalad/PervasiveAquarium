# Generated by Django 5.1.2 on 2024-10-11 11:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aquarium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thermostat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=50, unique=True)),
                ('default_temperature', models.DecimalField(decimal_places=2, max_digits=5)),
                ('installation_date', models.DateField(auto_now_add=True)),
                ('aquarium', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='aquarium.aquarium')),
            ],
        ),
        migrations.CreateModel(
            name='TemperatureLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('thermostat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aquarium.thermostat')),
            ],
        ),
    ]
