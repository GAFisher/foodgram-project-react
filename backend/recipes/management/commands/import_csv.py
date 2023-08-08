import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient

CSV_DIR = BASE_DIR / 'data' / 'ingredients.csv'


class Command(BaseCommand):
    help = 'Команда для загрузки списка ингредиентов в БД.'

    def import_ingredient(self):
        with open(CSV_DIR, 'r') as file:
            reader = csv.reader(file)
            ingredients = []

            for row in reader:
                ingredients.append(Ingredient(name=row[0], measurement_unit=row[1]))
            Ingredient.objects.bulk_create(ingredients)

        print('Заполнение БД завершено.')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print('Загрузка данных из csv в базу:')
        self.import_ingredient()
