"""
Django command to wait for DB to be available
"""

from django.core.management.base import BaseCommand

import time

from psycopg2 import OperationalError as PsyError

from django.db.utils import OperationalError


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Waiting for DB Connection ->')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsyError, OperationalError):
                self.stdout.write('Wait for DB , waiting for a second')
                time.sleep(1)

        self.stdout.write('DB Available now! ')
