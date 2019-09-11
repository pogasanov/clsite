import random

import factory
import factory.fuzzy
import factory.random
from django.conf.global_settings import LANGUAGES

from clsite.utils import random_number_exponential_delay
from profiles import signals
from profiles.models import Language
from profiles.utils import LAW_TYPE_TAGS_CHOICES, SUBJECTIVE_TAGS_CHOICES, COUNTRIES_CHOICES, _get_states_for_country

SEED_VALUE = 54321
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

    handle = factory.LazyAttributeSequence(lambda o, n: '-'.join(o.full_name.lower().split(' ')) + str(n))
    email = factory.Faker('email')
    full_name = factory.Faker('name')
    password = 'pbkdf2_sha256$150000$2bhhJByaRefj$YjOjogq8+zzorhEeQgTyLYFSZD+tOLgYNeOWbSYhIVg='

    phone = factory.Faker('msisdn')
    bio = factory.LazyFunction(lambda: "<p>" + "</p><p>".join(factory.Faker('paragraphs', nb=3).generate()) + "</p>")
    experience = factory.Faker('pyint', min_value=0, max_value=30, step=1)
    current_job = factory.Faker('job')
    size_of_clients = factory.Faker('pyint', min_value=0, max_value=3, step=1)
    preferred_communication_method = factory.Faker('pyint', min_value=0, max_value=3, step=1)
    law_type_tags = factory.List([get_random_law_type_tag() for x in range(random_number_exponential_delay(pr=0.25))])
    subjective_tags = [get_random_subjective_tag() for _ in
                       range(random_number_exponential_delay(pr=0.25, probability_of_none=0.0))]
    summary = factory.Faker('catch_phrase')
    website = factory.Faker('uri')
    twitter = factory.Faker('word')
    linkedin = factory.Faker('word')
    facebook = factory.Faker('word')

    address = factory.RelatedFactory(AddressFactory, 'profile')
    education = factory.RelatedFactoryList(EducationFactory, 'profile', size=random.randrange(3))
    jurisdiction = factory.RelatedFactoryList(JurisdictionFactory, 'profile', size=random.randrange(3))
    admissions = factory.RelatedFactoryList(AdmissionFactory, 'profile', size=random.randrange(3))
    lawschool = factory.RelatedFactory(LawSchoolFactory, 'profile')
    workexperience = factory.RelatedFactoryList(WorkExperienceFactory, 'profile', size=random.randrange(3))
    organization = factory.RelatedFactoryList(OrganizationFactory, 'profile', size=random.randrange(3))
    award = factory.RelatedFactoryList(AwardFactory, 'profile', size=random.randrange(3))
    language = factory.RelatedFactoryList(LanguageFactory, 'profile', size=random.randrange(3))
