# -*- coding: utf-8 -*-
""" management command for importing sentences from the Tatoeba's sentences CSV file to the database engine."""
import csv
# if using django in debug mode this will come on handy
from django import db
db.reset_queries()

from itertools import islice
from django.core.management.base import BaseCommand, CommandError
from sentence_finder.models import phrase

class Command(BaseCommand):
    help = 'Re-imports phrases from the Tatoeva database. It is needed to have the file sentences.csv in the root of Django (where the file manage.py is located)'

    def add_arguments(self, parser):
        parser.add_argument('languages', type=str, help='Comma separated languages (ISO 639-3) to import to db (example: spa,rus,eng')

    def get_data(self, languages):
        """ Helper function to retrieve data from the csv file in a generator, so memory usage will not be a problem.
    row[1] contains the language code in ISO 639-3. """
        with open("sentences.csv", "r") as csvfile:
            for row in csv.reader(csvfile, delimiter="\t"):
                if row[1] in languages:
                    yield phrase(phrase=row[2], language=row[1])

    def bulk_create_iter(self, iterable, batch_size=10000):
        """Bulk create supporting generators. Returns only count of created objects."""
        created = 0
        while True:
            objects = phrase.objects.bulk_create(islice(iterable, batch_size))
            created += len(objects)
            if not objects:
                break
        return created

    def handle(self, *args, **options):
        """Command processor. Receive all arguments and call to the appropiate helper functions."""
        languages = options["languages"].split(",")
        self.stdout.write("Extracting phrases for the following languages: {langs}".format(langs=languages))
        self.stdout.write("Removing data from database...")
        # we must delete all previous data as there are no way of Insert_of_update when adding rows in bulk.
        phrase.objects.all().delete()
        self.stdout.write("Importing new data...")
        data = self.get_data(languages)
        self.stdout.write(str(self.bulk_create_iter(data, 10000)))