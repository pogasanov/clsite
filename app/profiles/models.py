import os
import uuid

from clsite.storage_backends import variativeStorage
from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField, DateRangeField
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models

from .choices import CURRENCIES
from .utils import COUNTRIES_CHOICES


class Address(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, verbose_name='Profile', related_name='address')
    building = models.CharField(max_length=20, verbose_name='Building/Unit')
    street = models.CharField(max_length=200, verbose_name='Street')
    city = models.CharField(max_length=100, verbose_name='City', null=True, blank=True)
    state = models.CharField(max_length=100, verbose_name='State', null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name='Country', choices=COUNTRIES_CHOICES)
    zipcode = models.CharField(max_length=10, verbose_name='ZIP code')


class Education(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    school = models.CharField(max_length=100, verbose_name='School name')
    degree = models.CharField(max_length=100, verbose_name='Degree')
    graduation_date = models.DateField(verbose_name='date of graduation')


class Jurisdiction(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    country = models.CharField(max_length=100, verbose_name='Country', choices=COUNTRIES_CHOICES)
    state = models.CharField(max_length=100, verbose_name='State', null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name='City', null=True, blank=True)

    def __str__(self):
        if self.city and self.state:
            return f'{self.city} ({self.state}, {self.country})'

        city_or_state = self.city or self.state

        if city_or_state:
            return f'{city_or_state} ({self.country})'

        return self.country


class Admissions(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    city = models.CharField(max_length=100, verbose_name='City', null=True, blank=True)
    state = models.CharField(max_length=100, verbose_name='State', null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name='Country', choices=COUNTRIES_CHOICES)
    year = models.PositiveIntegerField(verbose_name='date of graduation')


class LawSchool(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    school = models.CharField(max_length=100, verbose_name='School name')
    city = models.CharField(max_length=100, verbose_name='City', null=True, blank=True)
    state = models.CharField(max_length=100, verbose_name='State', null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name='Country', choices=COUNTRIES_CHOICES)


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
                         ('PF', 'Professional fluency'),
                         ('CF', 'Conversational fluency'))

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    name = models.CharField(max_length=10, choices=LANGUAGES)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVEL)

    def __repr__(self):
        return '{} - {}'.format(self.name, self.proficiency_level)


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
    username = None
    full_name = models.CharField(max_length=100)

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

    law_type_tags = ArrayField(
        models.CharField(max_length=50),
        verbose_name='Law Type Tags', blank=True, null=True
    )
    subjective_tags = ArrayField(
        models.CharField(max_length=50),
        verbose_name='Subjective Tags', blank=True, null=True
    )
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
            reference = '-'.join(self.full_name.lower().split(' '))
            full_name_profiles = Profile.objects.filter(handle=reference).count()
            reference_id = str(full_name_profiles + 1) if full_name_profiles else ''
            self.handle = reference + reference_id
            self.save(*args, **kwargs)

    def photo_url_or_default(self):
        if self.photo:
            return self.photo.url
        return static('dummy-img.png')

    def user_unconfirmed_transaction(self):
        return self.requestee.filter(is_confirmed=None).order_by('-created_at').first()

    def _compile_headline(self):
        headline_format = '{tags} attorney{jurisdictions}'

        jurisdictions = ', '.join([str(j) for j in self.jurisdiction_set.all()])
        law_type_tags = ', '.join(self.law_type_tags or [])
        subjective_tags = ', '.join(self.subjective_tags or [])

        if jurisdictions:
            jurisdictions = f' in {jurisdictions}'

        if subjective_tags:
            subjective_tags = f' {subjective_tags}'

        if law_type_tags:
            law_type_tags = f' {law_type_tags}'

        return headline_format.format(
            jurisdictions=jurisdictions,
            tags=subjective_tags + law_type_tags
        )

    @property
    def headline(self):
        name_or_handle = self.full_name if self.full_name else self.handle
        return f'{name_or_handle}, the{self._compile_headline()}'

    def browsing_headline(self):
        return f'The{self._compile_headline()}'


class Transaction(models.Model):
    REVIEW_CHOICES = (
        ('SD', 'Strongly Disagree'),
        ('D', 'Disagree'),
        ('N', 'Neutral'),
        ('A', 'Agree'),
        ('SA', 'Strongly Agree')
    )
    CURRENCY_CHOICES = CURRENCIES

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(verbose_name='Transaction Date')

    requester = models.ForeignKey('Profile', on_delete=models.CASCADE,
                                  related_name='requester', verbose_name='Requester')
    proof_receipt_requester = models.ImageField(upload_to=get_image_path, storage=variativeStorage(),
                                                verbose_name='Transaction Proof', blank=True, null=True)
    requester_review = models.CharField(max_length=2, choices=REVIEW_CHOICES,
                                        default=None, verbose_name='Requester\'s Review')
    requester_recommendation = models.TextField(null=True, blank=True,
                                                default=None, verbose_name='Requester\'s recommendation')

    requestee = models.ForeignKey('Profile', on_delete=models.CASCADE,
                                  related_name='requestee', verbose_name='Requestee')
    requestee_review = models.CharField(max_length=2, choices=REVIEW_CHOICES,
                                        default=None, verbose_name='Requestee\'s Review', null=True)
    requestee_recommendation = models.TextField(null=True, blank=True,
                                                default=None, verbose_name='Requestee\'s recommendation')

    is_confirmed = models.NullBooleanField(default=None, verbose_name='Requestee Confirmed')
    is_verified = models.NullBooleanField(default=None, verbose_name='Verified from Admin')
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Transaction Amount')
    value_in_usd = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Value in USD', null=True,
                                       blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,
                                default='USD', verbose_name='Transaction Currency')
    is_requester_principal = models.BooleanField(default=False, verbose_name='Requester Payed')

    def save(self, *args, **kwargs):
        ext = self.proof_receipt_requester.name.split('.')[-1]
        self.proof_receipt_requester.name = f'{uuid.uuid4().hex}.{ext}'
        super(Transaction, self).save(*args, **kwargs)
