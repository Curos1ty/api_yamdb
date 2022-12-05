import csv
from django.core.management.base import BaseCommand

from reviews.models import GenreTitle


class Command(BaseCommand):
    """"Загрузка данных из файла genre_title.csv в базу данных."""

    help = 'Загрузка данных из файла genre_title.csv в базу данных'

    def handle(self, *args, **options):
        csv_file = open('static/data/genre_title.csv', 'r')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            genretitle = GenreTitle(
                id=row['id'],
                genre_id=row['genre_id'],
                title_id=row['title_id']
            )
            genretitle.save()

        self.stdout.write('Загрузка данных модели GenreTitle завершена')
