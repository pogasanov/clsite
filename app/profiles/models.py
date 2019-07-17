import os

from django.db import models
from django.contrib.postgres.fields import ArrayField, DateRangeField
from django.conf import settings, global_settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf.global_settings import LANGUAGES

from clsite.storage_backends import variativeStorage

from .choices import USA_STATES
from .utils import LANGUAGES_CHOICES


class Address(models.Model):
    USA_STATES = USA_STATES

    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, verbose_name='Profile', related_name='address')
    building = models.CharField(max_length=20, verbose_name='Building/Unit')
    street = models.CharField(max_length=200, verbose_name='Street')
    city = models.CharField(max_length=100, verbose_name='City')
    state = models.CharField(max_length=2, choices=USA_STATES, verbose_name='State')
    zipcode = models.CharField(max_length=10, verbose_name='ZIP code')


class Education(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    school = models.CharField(max_length=100, verbose_name='School name')
    degree = models.CharField(max_length=100, verbose_name='Degree')
    graduation_date = models.DateField(verbose_name='date of graduation')


class Admissions(models.Model):
    USA_STATES = USA_STATES

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    state = models.CharField(max_length=2, choices=USA_STATES, verbose_name='State')
    year = models.PositiveIntegerField(verbose_name='date of graduation')


class LawSchool(models.Model):
    USA_STATES = USA_STATES

    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    school = models.CharField(max_length=100, verbose_name='School name')
    state = models.CharField(max_length=2, choices=USA_STATES, verbose_name='State')


class WorkExperience(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    company_name = models.CharField(max_length=100, verbose_name='Company')
    position = models.CharField(max_length=100, verbose_name='Position')
    duration = DateRangeField(verbose_name='Duration')
    responsibility = models.TextField(verbose_name='Responsibility')


class Organization(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    name = models.CharField(max_length=100, verbose_name='Organization')
    position = models.CharField(max_length=100, verbose_name='Position/Designation')
    duration = DateRangeField(verbose_name='Duration')


class Award(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    title = models.CharField(max_length=100, verbose_name='Title')
    presented_by = models.CharField(max_length=100, verbose_name='Presented by')
    year = models.PositiveIntegerField(verbose_name='Year')
    description = models.TextField(verbose_name='Description')

class Language(models.Model):
    PROFICIENCY_LEVEL = (('NS', 'Native speaker'),
                        ('PF', 'professional fluency'),
                        ('CF', 'conversational fluency'))

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    name = models.CharField(max_length=10, choices=LANGUAGES)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVEL)

    class Meta:
        unique_together = ('profile', 'name')


def get_image_path(instance, filename):
    return os.path.join(filename)


class UserManager(BaseUserManager):
    """
    Custom model manager for User model with no username field.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)


class Profile(AbstractUser):
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
    LANGUAGES = LANGUAGES_CHOICES
    username = None

    handle = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name='Email address', unique=True)

    phone = models.CharField(max_length=20, verbose_name='Contact Number (Office)', blank=True)
    photo = models.ImageField(upload_to=get_image_path, storage=variativeStorage(), verbose_name='Profile Picture',
                              blank=True, null=True)
    bio = models.TextField(verbose_name='Overview (Bio)', blank=True)
    experience = models.CharField(max_length=100, verbose_name='Years of Practice/Experience', blank=True)
    current_job = models.CharField(max_length=200, verbose_name='Current Job/Affiliation/Law Firm', blank=True)
    size_of_clients = models.PositiveSmallIntegerField(choices=SIZE_OF_CLIENTS, verbose_name='Size of clients',
                                                       blank=True, null=True)
    preferred_communication_method = models.PositiveSmallIntegerField(choices=PREFERRED_COMMUNICATION_METHODS,
                                                                      verbose_name='Preferred communication method',
                                                                      blank=True, null=True)

    license_status = models.PositiveSmallIntegerField(choices=LICENSE_STATUSES, verbose_name='License Status',
                                                      blank=True, null=True)
    clients = ArrayField(
        models.CharField(max_length=100, verbose_name='Representative Clients'),
        blank=True, null=True
    )

    jurisdiction = ArrayField(
        models.CharField(max_length=2, choices=USA_STATES),
        verbose_name='Jurisdiction', blank=True, null=True
    )
    law_type_tags = ArrayField(
        models.CharField(max_length=50),
        verbose_name='Law Type Tags', blank=True, null=True
    )
    subjective_tags = ArrayField(
        models.CharField(max_length=50),
        verbose_name='Subjective Tags', blank=True, null=True
    )
    headline = models.CharField(max_length=120, verbose_name='Headline', blank=True)
    summary = models.CharField(max_length=140, verbose_name='Summary', blank=True)
    website = models.URLField(verbose_name='Website URL', blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    linkedin = models.CharField(max_length=50, blank=True)
    facebook = models.CharField(max_length=50, blank=True)

    publish_to_thb = models.BooleanField(default=False, verbose_name='Publish To THB')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if not self.handle:
            self.handle = self.email.split('@')[0] + str(self.id)
            self.save(*args, **kwargs)

    def photo_url_or_default(self):
        if self.photo:
            return self.photo.url
        return static('dummy-img.png')
