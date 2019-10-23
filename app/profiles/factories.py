import random

import factory
import factory.fuzzy
import factory.random
from django.conf.global_settings import LANGUAGES

from clsite.settings import SEED_VALUE, DEFAULT_USER_PASSWORD_HASH
from clsite.utils import random_number_exponential_delay
from profiles import signals
from profiles.models import Language, Profile
from profiles.utils import LAW_TYPE_TAGS_CHOICES, SUBJECTIVE_TAGS_CHOICES, COUNTRIES_CHOICES, _get_states_for_country

random.seed(SEED_VALUE)
factory.random.reseed_random(SEED_VALUE)


def get_random_law_type_tag():
    return random.choice(LAW_TYPE_TAGS_CHOICES)[0]


def get_random_subjective_tag():
    return random.choice(SUBJECTIVE_TAGS_CHOICES)[0]


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'profiles.Address'
        django_get_or_create = ('profile',)

    profile = factory.SubFactory('profiles.factories.ProfileFactory', address=None)
    country = factory.fuzzy.FuzzyChoice(COUNTRIES_CHOICES, getter=lambda c: c[0])
    state = factory.LazyAttribute(
        lambda o: random.choice(_get_states_for_country(o.country))[0] if _get_states_for_country(
            o.country) else None
    )
    city = factory.LazyAttribute(
        lambda o: factory.Faker('city').generate() if o.state else None
    )
    zipcode = factory.Faker('postalcode')
    street = factory.Faker('street_address')
    building = factory.Faker('building_number')


class EducationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'profiles.Education'

    profile = factory.SubFactory('profiles.factories.ProfileFactory', education=None)
    school = factory.Faker('company')
    degree = factory.LazyFunction(lambda: ' '.join(factory.Faker('words').generate()))
    graduation_date = factory.Faker('date_object')


class JurisdictionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'profiles.Jurisdiction'

    profile = factory.SubFactory('profiles.factories.ProfileFactory', jurisdiction=None)
    country = factory.fuzzy.FuzzyChoice(COUNTRIES_CHOICES, getter=lambda c: c[0])
    state = factory.LazyAttribute(
        lambda o: random.choice(_get_states_for_country(o.country))[0] if _get_states_for_country(o.country) else None
    )
    city = factory.LazyAttribute(
        lambda o: factory.Faker('city').generate() if o.state else None
    )


class AdmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'profiles.Admissions'

    profile = factory.SubFactory('profiles.factories.ProfileFactory', admissions=None)
    country = factory.fuzzy.FuzzyChoice(COUNTRIES_CHOICES, getter=lambda c: c[0])
    state = factory.LazyAttribute(
        lambda o: random.choice(_get_states_for_country(o.country))[0] if _get_states_for_country(o.country) else None
    )
    city = factory.LazyAttribute(
        lambda o: factory.Faker('city').generate() if o.state else None
    )
    year = factory.Faker('pyint', min_value=1990, max_value=2019, step=1)


class LawSchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'profiles.LawSchool'
        django_get_or_create = ('profile',)

    profile = factory.SubFactory('profiles.factories.ProfileFactory', lawschool=None)
    country = factory.fuzzy.FuzzyChoice(COUNTRIES_CHOICES, getter=lambda c: c[0])
    state = factory.LazyAttribute(
        lambda o: random.choice(_get_states_for_country(o.country))[0] if _get_states_for_country(o.country) else None
    )
    city = factory.LazyAttribute(
        lambda o: factory.Faker('city').generate() if o.state else None
    )
    school = factory.Faker('company')


class WorkExperienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'profiles.WorkExperience'

    profile = factory.SubFactory('profiles.factories.ProfileFactory', workexperience=None)
    company_name = factory.Faker('company')
    position = factory.Faker('job')
    responsibility = factory.LazyFunction(lambda: '\n'.join(factory.Faker('paragraphs', nb=3).generate()))

    @factory.lazy_attribute
    def duration(self):
        end_date = factory.Faker('date_object').generate()
        start_date = factory.Faker('date', pattern='%Y-%m-%d', end_datetime=end_date).generate()
        return f"[{start_date},{end_date})"


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'profiles.Organization'

    profile = factory.SubFactory('profiles.factories.ProfileFactory', organization=None)
    name = factory.Faker('company')
    position = factory.Faker('job')

    @factory.lazy_attribute
    def duration(self):
        end_date = factory.Faker('date_object').generate()
        start_date = factory.Faker('date', pattern='%Y-%m-%d', end_datetime=end_date).generate()
        return f"[{start_date},{end_date})"


class AwardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'profiles.Award'

    profile = factory.SubFactory('profiles.factories.ProfileFactory', award=None)
    title = factory.Faker('word')
    presented_by = factory.Faker('company')
    year = factory.Faker('pyint', min_value=1990, max_value=2019, step=1)
    description = factory.LazyFunction(lambda: '\n'.join(factory.Faker('paragraphs', nb=3).generate()))


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'profiles.Language'

    profile = factory.SubFactory('profiles.factories.ProfileFactory', language=None)
    name = factory.fuzzy.FuzzyChoice(LANGUAGES, getter=lambda c: c[0])
    proficiency_level = factory.fuzzy.FuzzyChoice(Language.PROFICIENCY_LEVEL, getter=lambda c: c[0])


@factory.django.mute_signals(signals.post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'profiles.Profile'
        django_get_or_create = ('handle', 'email')

    class Params:
        empty_profile = factory.Trait(
            register_status=Profile.REGISTER_STATUS_EMPTY_PROFILE,

            full_name='',

            phone='',
            bio='',
            experience='',
            current_job='',
            size_of_clients=None,
            preferred_communication_method=None,
            law_type_tags=None,
            subjective_tags=None,
            summary='',
            website='',
            twitter='',
            linkedin='',
            facebook='',

            address=None,
            education=None,
            jurisdiction=None,
            admissions=None,
            lawschool=None,
            workexperience=None,
            organization=None,
            award=None,
            language=None,
        )

        email_not_confirmed = factory.Trait(
            email_confirmed_at=None
        )

    register_status = Profile.REGISTER_STATUS_COMPLETE

    handle = factory.LazyAttributeSequence(lambda o, n: '-'.join(o.full_name.lower().split(' ')) + str(n))
    email = factory.Sequence(lambda n: factory.Faker('email').generate() + str(n))
    email_confirmed_at = factory.Faker('date_between', start_date="-3y", end_date="today")
    full_name = factory.Faker('name')
    password = DEFAULT_USER_PASSWORD_HASH

    phone = factory.LazyFunction(lambda: factory.Faker('msisdn').generate() if random.random() < 0.5 else '')
    bio = factory.LazyFunction(lambda: "<p>" + "</p><p>".join(
        factory.Faker('paragraphs', nb=3).generate()) + "</p>" if random.random() < 0.5 else '')
    experience = factory.LazyFunction(
        lambda: factory.Faker('pyint', min_value=0, max_value=30, step=1).generate() if random.random() < 0.5 else '')
    current_job = factory.LazyFunction(
        lambda: factory.Faker('job').generate() if random.random() < 0.5 else '')
    size_of_clients = factory.LazyFunction(
        lambda: factory.Faker('pyint', min_value=0, max_value=3, step=1).generate() if random.random() < 0.5 else None)
    preferred_communication_method = factory.LazyFunction(
        lambda: factory.Faker('pyint', min_value=0, max_value=3, step=1).generate() if random.random() < 0.5 else None)
    law_type_tags = factory.LazyFunction(
        lambda: [get_random_law_type_tag() for _ in range(random_number_exponential_delay(pr=0.25))])
    subjective_tags = factory.LazyFunction(
        lambda: [get_random_subjective_tag() for _ in
                 range(random_number_exponential_delay(pr=0.25, probability_of_none=0.0))])
    summary = factory.LazyFunction(lambda: factory.Faker('catch_phrase').generate() if random.random() < 0.5 else '')
    website = factory.LazyFunction(lambda: factory.Faker('uri').generate() if random.random() < 0.5 else '')
    twitter = factory.LazyFunction(lambda: factory.Faker('word').generate() if random.random() < 0.5 else '')
    linkedin = factory.LazyFunction(lambda: factory.Faker('word').generate() if random.random() < 0.5 else '')
    facebook = factory.LazyFunction(lambda: factory.Faker('word').generate() if random.random() < 0.5 else '')

    address = factory.RelatedFactory(AddressFactory, 'profile')
    education = factory.RelatedFactoryList(EducationFactory, 'profile', size=lambda: random.randrange(3))
    jurisdiction = factory.RelatedFactoryList(JurisdictionFactory, 'profile', size=lambda: random.randrange(3))
    admissions = factory.RelatedFactoryList(AdmissionFactory, 'profile', size=lambda: random.randrange(3))
    lawschool = factory.RelatedFactory(LawSchoolFactory, 'profile')
    workexperience = factory.RelatedFactoryList(WorkExperienceFactory, 'profile', size=lambda: random.randrange(3))
    organization = factory.RelatedFactoryList(OrganizationFactory, 'profile', size=lambda: random.randrange(3))
    award = factory.RelatedFactoryList(AwardFactory, 'profile', size=lambda: random.randrange(3))
    language = factory.RelatedFactoryList(LanguageFactory, 'profile', size=lambda: random.randrange(3))
