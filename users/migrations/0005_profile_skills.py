# Generated by Django 4.2.5 on 2023-10-20 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_location_skill'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(blank=True, to='users.skill'),
        ),
    ]
