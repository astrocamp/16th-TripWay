# Generated by Django 5.0.4 on 2024-05-08 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0004_remove_spots_list_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spots_list',
            name='deleted_at',
        ),
    ]