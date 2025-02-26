# Generated by Django 2.2.4 on 2019-09-05 01:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('transactions', '0003_auto_20190904_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='is_requester_principal',
            field=models.BooleanField(choices=[(True, 'I paid them'), (False, 'They paid me')], default=False,
                                      verbose_name='Did one of you pay the other?'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='requestee_review',
            field=models.CharField(
                choices=[('SD', 'Strongly Disagree'), ('D', 'Disagree'), ('N', 'Neutral'), ('A', 'Agree'),
                         ('SA', 'Strongly Agree')], default='N', max_length=2,
                verbose_name='Would you work with them again?'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='requester_review',
            field=models.CharField(
                choices=[('SD', 'Strongly Disagree'), ('D', 'Disagree'), ('N', 'Neutral'), ('A', 'Agree'),
                         ('SA', 'Strongly Agree')], default='N', max_length=2, verbose_name="Requester's Review"),
        ),
    ]
