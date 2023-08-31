from django.core.management.base import BaseCommand
from expenses.models import Category, Subcategory
import json


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('./expenses/fixtures/categories_ro.json', 'r') as f:
            data = json.load(f)

        # for item in data['categories']:
        #     cat = item['name']
        #     emoji = item['emoji_text']
        #     Category.objects.create(name=cat, emoji_text=emoji)

        for item in data['categories']:
            subcats = item['subcategories']
            cat = item['name']
            for item in subcats:
                print(cat)
                print(item)
                category = Category.objects.get(name=cat)
                Subcategory.objects.create(name=item, category_id=category)
