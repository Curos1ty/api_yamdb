import csv

from django.core.management.base import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):
    """"Загрузка данных из файла genre.csv в базу данных."""

    help = 'Загрузка данных из файла genre.csv в базу данных'

    def handle(self, *args, **options):
        csv_file = open('static/data/genre.csv', 'r', encoding='utf-8')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genre.save()

        self.stdout.write('Загрузка данных модели Genre завершена')
