# Generated by Django 5.0.4 on 2024-05-16 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_delete_photo_trip_trips_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='trips_image',
            new_name='trip_image',
        ),
    ]
