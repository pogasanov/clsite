# Generated by Django 2.2.3 on 2019-08-02 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0029_remove_profile_headline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='proficiency_level',
            field=models.CharField(choices=[('NS', 'Native speaker'), ('PF', 'Professional fluency'), ('CF', 'Conversational fluency')], max_length=20),
        ),
    ]
