# Generated by Django 5.1.5 on 2025-01-22 03:38

import django.contrib.gis.db.models.fields
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
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('cancelled', 'cancelled'), ('ended', 'ended')], default='active', max_length=255)),
                ('event_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'event',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('entry_time', models.DateTimeField(blank=True, null=True)),
                ('departure_time', models.DateTimeField(blank=True, null=True)),
                ('location_attendance', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('type_data', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
            options={
                'db_table': 'attendance',
                'unique_together': {('user', 'event')},
            },
        ),
    ]
