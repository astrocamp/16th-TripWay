# Generated by Django 5.0.4 on 2024-05-21 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0002_spot_city_spot_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='name',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
