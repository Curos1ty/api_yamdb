import csv

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Загрузка данных из файла users.csv в базу данных."""

    help = 'Загрузка данных из файла users.csv в базу данных'

    def handle(self, *args, **options):
        csv_file = open('static/data/users.csv', 'r', encoding='utf-8')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            review = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            review.save()

        self.stdout.write('Загрузка данных модели User завершена')
