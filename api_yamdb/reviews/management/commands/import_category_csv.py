import csv
from django.core.management.base import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    """Загрузка данных из файла category.csv в базу данных."""

    help = 'Загрузка данных из файла category.csv в базу данных'

    def handle(self, *args, **options):
        csv_file = open('static/data/category.csv', 'r', encoding='utf-8')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()

        self.stdout.write('Загрузка данных модели Category завершена')
