# Generated by Django 4.1 on 2022-09-19 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
