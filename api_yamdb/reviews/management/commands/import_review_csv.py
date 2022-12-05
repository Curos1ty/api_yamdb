import csv

from django.core.management.base import BaseCommand

from reviews.models import Review


class Command(BaseCommand):
    """Загрузка данных из файла review.csv в базу данных."""

    help = 'Загрузка данных из файла review.csv в базу данных'

    def handle(self, *args, **options):
        csv_file = open('static/data/review.csv', 'r', encoding='utf-8')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            review = Review(
                id=row['id'],
                text=row['text'],
                score=row['score'],
                pub_date=row['pub_date'],
                author_id=row['author'],
                title_id=row['title_id']
            )
            review.save()

        self.stdout.write('Загрузка данных модели Review завершена')
