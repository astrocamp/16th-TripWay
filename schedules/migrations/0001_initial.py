# Generated by Django 5.0.4 on 2024-05-21 18:44

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("spots", "0001_initial"),
        ("trips", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("spot_name", models.CharField(max_length=100)),
                (
                    "start_time",
                    models.TimeField(default=django.utils.timezone.now, null=True),
                ),
                (
                    "end_time",
                    models.TimeField(default=django.utils.timezone.now, null=True),
                ),
                ("note", models.TextField(null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(null=True)),
                (
                    "spot",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="spots.spot",
                    ),
                ),
                (
                    "trip",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="trips.trip",
                    ),
                ),
            ],
        ),
    ]
