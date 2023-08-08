import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient

CSV_DIR = BASE_DIR.parent / 'data' / 'ingredients.csv'


class Command(BaseCommand):
    help = 'Команда для загрузки списка ингредиентов в БД.'

    def import_ingredient(self):
        with open(CSV_DIR, 'r') as file:
            reader = csv.reader(file)

            # как я понял, делать нужно так
            #
            # result = set()
            #
            # for row in reader:
            #     result.add(Ingredient(name=row[0], measurement_unit=row[1]))
            #
            # Ingredient.objects.bulk_create(result)
            #
            # так как ты используешь сет - повторов не будет - попробуй

            for row in reader:
                try:
                    obj, created = Ingredient.objects.get_or_create(
                        name=row[0], measurement_unit=row[1]
                    )
                    if not created:
                        print(f'Модель Ingredient уже содержит {obj}')
                except Exception as error:
                    print(
                        f'Не удалось загрузить {row} в БД, ошибка {error}'
                    )
        print('Заполнение БД завершено.')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print('Загрузка данных из csv в базу:')
        self.import_ingredient()
