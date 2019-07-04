# Generated by Django 2.2.3 on 2019-07-04 22:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0021_profile_publish_to_thb'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('proof_receipt_requester', models.ImageField(blank=True, null=True, upload_to=profiles.models.get_image_path, verbose_name="Requester's Transaction Proof")),
                ('requester_review', models.CharField(choices=[('SD', 'Strongly Disagree'), ('D', 'Disagree'), ('N', 'Neutral'), ('A', 'Agree'), ('SA', 'Strongly Agree')], default=None, max_length=2, verbose_name="Requester's Review")),
                ('requester_recommendation', models.TextField(blank=True, default=None, null=True, verbose_name="Requester's recommendation")),
                ('requestee_review', models.CharField(choices=[('SD', 'Strongly Disagree'), ('D', 'Disagree'), ('N', 'Neutral'), ('A', 'Agree'), ('SA', 'Strongly Agree')], default=None, max_length=2, verbose_name="Requestee's Review")),
                ('requestee_recommendation', models.TextField(blank=True, default=None, null=True, verbose_name="Requestee's recommendation")),
                ('proof_receipt_requestee', models.ImageField(blank=True, null=True, upload_to=profiles.models.get_image_path, verbose_name="Requestee's Transaction Proof")),
                ('is_confirmed', models.NullBooleanField(default=None, verbose_name='Confirmed from Requestee')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Verified from Admin')),
                ('amount', models.FloatField(verbose_name='Amount of Transaction')),
                ('is_requester_principal', models.BooleanField(default=False, verbose_name='Requester Payed')),
                ('requestee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requestee', to=settings.AUTH_USER_MODEL, verbose_name='Requestee')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL, verbose_name='Requester')),
            ],
        ),
    ]
