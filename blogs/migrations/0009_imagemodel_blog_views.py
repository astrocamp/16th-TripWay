# Generated by Django 5.0.6 on 2024-06-13 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0008_remove_blogcomment_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('spot_name', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
