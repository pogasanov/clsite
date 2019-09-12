from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from transactions.factories import TransactionFactory


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('transactions_count', nargs='?', type=int, default=100)

    def handle(self, *args, **options):
        try:
            TransactionFactory.create_batch(options['transactions_count'])
        except IntegrityError as ie:
            raise CommandError('Unable to generate dummy profiles, truncate your database and try again.', ie)
        except Exception as ex:
            raise CommandError('Unable to generate dummy profiles.', ex)
