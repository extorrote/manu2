# Generated by Django 5.1.4 on 2025-01-24 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('development_name', models.CharField(blank=True, max_length=50, null=True)),
                ('neighborhood', models.CharField(blank=True, max_length=50, null=True)),
                ('holiday_season', models.CharField(blank=True, max_length=50, null=True)),
                ('summer_and_fall', models.CharField(blank=True, max_length=50, null=True)),
                ('winter_and_spring', models.CharField(blank=True, max_length=50, null=True)),
                ('refundable_damage_deposit', models.CharField(blank=True, max_length=50, null=True)),
                ('night_minimum', models.CharField(blank=True, max_length=50, null=True)),
                ('primary_view', models.CharField(blank=True, max_length=50, null=True)),
                ('bedrooms', models.CharField(blank=True, max_length=50, null=True)),
                ('bathrooms', models.CharField(blank=True, max_length=50, null=True)),
                ('property_type', models.CharField(blank=True, max_length=200, null=True)),
                ('max_people', models.PositiveIntegerField()),
                ('children_under_12', models.CharField(blank=True, max_length=50, null=True)),
                ('pet_friendly', models.CharField(blank=True, max_length=50, null=True)),
                ('secondary_view', models.CharField(blank=True, max_length=50, null=True)),
                ('imagen1', models.ImageField(blank=True, null=True, upload_to='manuelapp/images_rentals')),
                ('imagen2', models.ImageField(blank=True, null=True, upload_to='manuelapp/images_rentals')),
                ('imagen3', models.ImageField(blank=True, null=True, upload_to='manuelapp/images_rentals')),
                ('imagen4', models.ImageField(blank=True, null=True, upload_to='manuelapp/images_rentals')),
                ('imagen5', models.ImageField(blank=True, null=True, upload_to='manuelapp/images_rentals')),
                ('imagen6', models.ImageField(blank=True, null=True, upload_to='manuelapp/images_rentals')),
                ('imagen7', models.ImageField(blank=True, null=True, upload_to='manuelapp/images_rentals')),
                ('imagen8', models.ImageField(blank=True, null=True, upload_to='manuelapp/images_rentals')),
                ('video', models.FileField(blank=True, null=True, upload_to='manuelapp/images_rentals')),
                ('hot_water', models.CharField(blank=True, max_length=500, null=True)),
                ('air_conditioning', models.CharField(blank=True, max_length=150, null=True)),
                ('smoking_allowed', models.CharField(blank=True, max_length=50, null=True)),
                ('on_site_gym', models.CharField(blank=True, max_length=50, null=True)),
                ('swimming_pool', models.CharField(blank=True, max_length=50, null=True)),
                ('appliances', models.CharField(blank=True, max_length=250, null=True)),
                ('security', models.BooleanField(default=False)),
                ('google_maps', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('num_guests', models.IntegerField()),
                ('special_requests', models.TextField(blank=True)),
                ('condo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='manuelapp.condo')),
            ],
        ),
    ]
