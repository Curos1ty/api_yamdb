import csv
from django.core.management.base import BaseCommand

from reviews.models import Comment


class Command(BaseCommand):
    """Загрузка данных из файла comments.csv в базу данных."""

    help = 'Загрузка данных из файла comments.csv в базу данных'

    def handle(self, *args, **options):
        csv_file = open('static/data/comments.csv', 'r', encoding='utf-8')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            review = Comment(
                id=row['id'],
                text=row['text'],
                pub_date=row['pub_date'],
                author_id=row['author'],
                review_id=row['review_id']
            )
            review.save()

        self.stdout.write('Загрузка данных модели Comment завершена')
