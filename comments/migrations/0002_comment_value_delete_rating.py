# Generated by Django 5.0.4 on 2024-05-26 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='value',
            field=models.IntegerField(default=None),
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]