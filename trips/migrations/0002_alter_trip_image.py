# Generated by Django 5.0.6 on 2024-05-30 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='trips_coverPhoto/'),
        ),
    ]
