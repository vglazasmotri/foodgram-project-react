import csv
import sys

from django.core.management.base import BaseCommand

from foodgram_backend.settings import DATA_ROOT
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из csv файла в базу данных.'

    def add_arguments(self, parser):
        parser.add_argument(
            'path_file',
            type=str,
            help='Указывает путь к файлу с фикстурами.',
        )

    def handle(self, *args, **kwargs):
        path_file = kwargs['path_file']
        try:
            with open(
                f'{DATA_ROOT}/{path_file}',
                encoding='utf-8',
            ) as file:
                reader = csv.reader(file)
                next(reader)
                ingredients = [
                    Ingredient(
                        name=extracted_name,
                        measurement_unit=extracted_unit,
                    )
                    for extracted_name, extracted_unit in reader
                ]
                Ingredient.objects.bulk_create(ingredients)
        except ValueError:
            sys.stdout.write("Ошибка! Неверный тип данных!")
        else:
            sys.stdout.write("Данные загружены!")
