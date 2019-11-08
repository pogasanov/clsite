import random

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from profiles.models import Profile
from transactions.factories import TransactionFactory


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('transactions_count', nargs='?', type=int, default=1000)
        parser.add_argument('--generate-profiles', action='store_true')

    def handle(self, *args, **options):
        try:
            if options['generate_profiles']:
                TransactionFactory.create_batch(options['transactions_count'])
            else:
                profiles = list(Profile.objects.all())
                if not profiles:
                    raise CommandError('You need to generate profiles first. Use generateprofiles command.')
                for _ in range(options['transactions_count']):
                    created_by, sent_to = random.sample(profiles, 2)
                    TransactionFactory(created_by=created_by, sent_to=sent_to)
        except IntegrityError as ie:
            raise CommandError('Unable to generate dummy profiles, truncate your database and try again.', ie)
        except Exception as ex:
            raise CommandError('Unable to generate dummy profiles.', ex)
