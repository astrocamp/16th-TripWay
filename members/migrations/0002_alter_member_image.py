# Generated by Django 5.0.6 on 2024-06-08 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to=''),
        ),
    ]