# Generated by Django 2.2.5 on 2019-10-14 00:57

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_auto_20190923_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='is_admin_approved',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='is_proof_by_requester',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='requestee_recommendation',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='requestee_review',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='requester_recommendation',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='requester_review',
        ),
        migrations.AddField(
            model_name='transaction',
            name='is_flagged',
            field=models.BooleanField(default=False, verbose_name='Flagged'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='proof_receipt',
            field=models.ImageField(upload_to=profiles.models.get_image_path, verbose_name='Transaction Proof'),
        ),
    ]
