from django.core.management.base import BaseCommand

from main.models import Category


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        category_name_options = Category.OPTIONS
        list_of_categories = [item[0] for item in category_name_options]

        for category in list_of_categories:
            Category.objects.get_or_create(name=category)
