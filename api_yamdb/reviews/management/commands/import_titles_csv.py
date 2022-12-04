import csv
from django.core.management.base import BaseCommand

from reviews.models import Title


class Command(BaseCommand):
    """Загрузка данных из файла titles.csv в базу данных."""

    help = 'Загрузка данных из файла titles.csv в базу данных'

    def handle(self, *args, **options):
        csv_file = open('static/data/titles.csv', 'r', encoding='utf-8')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category']
            )
            title.save()

        self.stdout.write('Загрузка данных модели Title завершена')
