# Generated by Django 2.2.2 on 2019-06-10 04:38

from django.db import migrations, models
import profiles.models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='dummy-img.png', storage=storages.backends.s3boto3.S3Boto3Storage, upload_to=profiles.models.get_image_path),
        ),
    ]
