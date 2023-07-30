import csv
from django.core.management.base import BaseCommand
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient

CSV_DIR = BASE_DIR.parent / 'data' / 'ingredients.csv'


class Command(BaseCommand):
    help = 'Команда для загрузки списка ингредиентов в базу данных.'

    def import_ingredient(self):
        with open(CSV_DIR, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    obj, created = Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1]
                    )
                    if not created:
                        print(f'Модель Ingredient уже содержит {obj}')
                except Exception as error:
                    print(f'Не удалось загрузить {row} в базу данных, ошибка {error}')
        print('Заполнение базы данных завершено.')

    def handle(self, *args, **kwargs):
        print('Загрузка данных из csv в базу:')
        self.import_ingredient()
