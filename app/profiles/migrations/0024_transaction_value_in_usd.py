# Generated by Django 2.2.3 on 2019-07-14 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0023_merge_20190711_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='value_in_usd',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True, verbose_name='Value in USD'),
        ),
    ]
