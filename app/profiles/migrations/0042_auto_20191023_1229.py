# Generated by Django 2.2.6 on 2019-10-23 12:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('profiles', '0041_remove_profile_register_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_confirmed_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
