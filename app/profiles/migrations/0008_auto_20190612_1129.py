# Generated by Django 2.2.2 on 2019-06-12 11:29

import django.contrib.postgres.fields
import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20190612_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('presented_by', models.CharField(max_length=100, verbose_name='Presented by')),
                ('year', models.PositiveIntegerField(verbose_name='Year')),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='LawSchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=100, verbose_name='School name')),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2, verbose_name='State')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Organization')),
                ('position', models.CharField(max_length=100, verbose_name='Position/Designation')),
                ('duration', django.contrib.postgres.fields.ranges.DateRangeField(verbose_name='Duration')),
            ],
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, verbose_name='Company')),
                ('position', models.CharField(max_length=100, verbose_name='Position')),
                ('duration', django.contrib.postgres.fields.ranges.DateRangeField(verbose_name='Duration')),
                ('responsibility', models.TextField(verbose_name='Responsibility')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='clients',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100, verbose_name='Representative Clients'), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='profile',
            name='languages',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('dsb', 'Lower Sorbian'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-co', 'Colombian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gd', 'Scottish Gaelic'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hsb', 'Upper Sorbian'), ('hu', 'Hungarian'), ('hy', 'Armenian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kab', 'Kabyle'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmål'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese')], max_length=10, verbose_name='Languages'), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='profile',
            name='license_status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Active'), (1, 'In good standing')], null=True, verbose_name='License Status'),
        ),
        migrations.AddField(
            model_name='profile',
            name='associations',
            field=models.ManyToManyField(blank=True, null=True, to='profiles.Organization'),
        ),
        migrations.AddField(
            model_name='profile',
            name='awards',
            field=models.ManyToManyField(blank=True, null=True, to='profiles.Award'),
        ),
        migrations.AddField(
            model_name='profile',
            name='law_school',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='profiles.LawSchool'),
        ),
        migrations.AddField(
            model_name='profile',
            name='work_experiences',
            field=models.ManyToManyField(blank=True, null=True, to='profiles.WorkExperience'),
        ),
    ]
