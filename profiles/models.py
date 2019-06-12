from django.db import models
from django.contrib.postgres.fields import ArrayField, DateRangeField
from django.conf import settings, global_settings
from clsite.storage_backends import variativeStorage
import os

from .choices import USA_STATES


class Address(models.Model):
    USA_STATES = USA_STATES

    building = models.CharField(max_length=20, verbose_name='Building/Unit')
    street = models.CharField(max_length=200, verbose_name='Street')
    city = models.CharField(max_length=100, verbose_name='City')
    state = models.CharField(max_length=2, choices=USA_STATES, verbose_name='State')
    zipcode = models.CharField(max_length=10, verbose_name='ZIP code')


class Education(models.Model):
    school = models.CharField(max_length=100, verbose_name='School name')
    degree = models.CharField(max_length=100, verbose_name='Degree')
    graduation_date = models.DateField(verbose_name='date of graduation')


class Admissions(models.Model):
    USA_STATES = USA_STATES

    state = models.CharField(max_length=2, choices=USA_STATES, verbose_name='State')
    year = models.PositiveIntegerField(verbose_name='date of graduation')


class LawSchool(models.Model):
    USA_STATES = USA_STATES

    school = models.CharField(max_length=100, verbose_name='School name')
    state = models.CharField(max_length=2, choices=USA_STATES, verbose_name='State')


class WorkExperience(models.Model):
    company_name = models.CharField(max_length=100, verbose_name='Company')
    position = models.CharField(max_length=100, verbose_name='Position')
    duration = DateRangeField(verbose_name='Duration')
    responsibility = models.TextField(verbose_name='Responsibility')


class Organization(models.Model):
    name = models.CharField(max_length=100, verbose_name='Organization')
    position = models.CharField(max_length=100, verbose_name='Position/Designation')
    duration = DateRangeField(verbose_name='Duration')


class Award(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    presented_by = models.CharField(max_length=100, verbose_name='Presented by')
    year = models.PositiveIntegerField(verbose_name='Year')
    description = models.TextField(verbose_name='Description')


def get_image_path(instance, filename):
    return os.path.join(filename)


class Profile(models.Model):
    USA_STATES = USA_STATES
    SIZE_OF_CLIENTS = (
        (0, 'Individuals'),
        (1, 'Small businesses (1-100 people)'),
        (2, 'Medium businesses (100-1000 people)'),
        (3, 'Large businesses (1000 upwards)')
    )
    PREFERRED_COMMUNICATION_METHODS = (
        (0, 'Whatsapp'),
        (1, 'Email'),
        (2, 'Call'),
        (3, 'In-Person')
    )
    LICENSE_STATUSES = (
        (0, 'Active'),
        (1, 'In good standing')
    )
    LANGUAGES = global_settings.LANGUAGES

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.PROTECT, verbose_name='Work Address', blank=True,
                                   null=True)
    phone = models.CharField(max_length=20, verbose_name='Contact Number (Office)', blank=True)
    photo = models.ImageField(upload_to=get_image_path, default='dummy-img.png', storage=variativeStorage(),
                              verbose_name='Profile Picture')
    education = models.OneToOneField(Education, on_delete=models.PROTECT, verbose_name='Education', blank=True,
                                     null=True)
    bio = models.TextField(verbose_name='Overview (Bio)', blank=True)
    experience = models.CharField(max_length=100, verbose_name='Years of Practice/Experience', blank=True)
    email = models.EmailField(verbose_name='Email', blank=True)
    current_job = models.CharField(max_length=200, verbose_name='Current Job/Affiliation/Law Firm', blank=True)
    size_of_clients = models.PositiveSmallIntegerField(choices=SIZE_OF_CLIENTS, verbose_name='Size of clients',
                                                       blank=True, null=True)
    preferred_communication_method = models.PositiveSmallIntegerField(choices=PREFERRED_COMMUNICATION_METHODS,
                                                                      verbose_name='Preferred communication method',
                                                                      blank=True, null=True)

    license_status = models.PositiveSmallIntegerField(choices=LICENSE_STATUSES, verbose_name='License Status',
                                                      blank=True, null=True)
    languages = ArrayField(
        models.CharField(max_length=10, choices=LANGUAGES, verbose_name='Languages'),
        blank=True, null=True
    )
    law_school = models.OneToOneField(LawSchool, on_delete=models.PROTECT, blank=True, null=True)
    work_experiences = models.ManyToManyField(WorkExperience, blank=True)
    associations = models.ManyToManyField(Organization, blank=True)
    clients = ArrayField(
        models.CharField(max_length=100, verbose_name='Representative Clients'),
        blank=True, null=True
    )
    awards = models.ManyToManyField(Award, blank=True)

    jurisdiction = ArrayField(
        models.CharField(max_length=2, choices=USA_STATES),
        verbose_name='Jurisdiction', blank=True, null=True
    )
    headline = models.CharField(max_length=120, verbose_name='Headline', blank=True)
    website = models.URLField(verbose_name='Website URL', blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    linkedin = models.CharField(max_length=50, blank=True)
    facebook = models.CharField(max_length=50, blank=True)
