from django.core.management.base import BaseCommand, CommandError
from ...models import *


class Command(BaseCommand):
    help = 'Удаление всех новостей из данной категории'

    def add_arguments(self, parser):
        parser.add_argument('category_name', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category_name"]}? yes/no\n')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))

        category_name = options['category_name']

        if answer == 'yes':

            try:
                category = Category.objects.get(name=category_name)
                Post.objects.filter(postCategory=category).delete()
                self.stdout.write(self.style.SUCCESS(
                    f'Succesfully deleted all news from category {category.name}'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category {category_name}'))