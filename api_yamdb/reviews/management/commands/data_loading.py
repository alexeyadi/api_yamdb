import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for model, csv_file in TABLES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_file}',
                'r',
                encoding='utf-8'
            ) as csv_files:
                reader = csv.DictReader(csv_files)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
