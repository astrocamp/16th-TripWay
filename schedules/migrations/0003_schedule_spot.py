# Generated by Django 5.0.4 on 2024-05-14 09:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_schedule_trip'),
        ('spots', '0002_spot_city_spot_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='spot',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='spots.spot'),
        ),
    ]
