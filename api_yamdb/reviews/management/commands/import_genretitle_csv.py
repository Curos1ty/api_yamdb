import csv

from django.core.management.base import BaseCommand

from reviews.models import Genre, Title


class Command(BaseCommand):
    """"Загрузка данных из файла genre_title.csv в базу данных."""

    help = 'Загрузка данных из файла genre_title.csv в базу данных'

    def handle(self, *args, **options):
        csv_file = open('static/data/genre_title.csv', 'r')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            title = Title.objects.get(pk=row['title_id'])
            genre = Genre.objects.get(pk=row['genre_id'])
            title.genre.add(genre)

        self.stdout.write('Загрузка данных для таблицы genretitle завершена')
