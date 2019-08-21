from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from profiles.faker import generate_profiles


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('profiles_count', type=int)

    def handle(self, *args, **options):
        try:
            generate_profiles(options['profiles_count'])
        except IntegrityError as ie:
            raise CommandError('Unable to generate dummy profiles, truncate your database and try again.', ie)
        except Exception as ex:
            raise CommandError('Unable to generate dummy profiles.', ex)
