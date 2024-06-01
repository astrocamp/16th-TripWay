# Generated by Django 5.0.6 on 2024-05-31 06:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('spots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('value', models.IntegerField(default=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('spot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spots.spot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
