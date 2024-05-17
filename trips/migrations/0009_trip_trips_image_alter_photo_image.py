# Generated by Django 5.0.4 on 2024-05-17 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0008_photo_remove_trip_cover_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='trips_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='image/'),
        ),
    ]
