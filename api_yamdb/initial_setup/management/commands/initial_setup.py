import csv
import logging

from django.contrib.staticfiles import finders

from django.core.management import BaseCommand

from review.models import User, Category, Gener, Title

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = ('Upload database with initial configuration data. '
            'Must be triggered after migrations')

    def add_arguments(self, parser):
        parser.add_argument('--add_users',
                            action='store_true',
                            help='Add users', )

        parser.add_argument('--add_category',
                            action='store_true',
                            help='Add categories', )

        parser.add_argument('--add_gener',
                            action='store_true',
                            help='Add genres', )

        parser.add_argument('--add_titles',
                            action='store_true',
                            help='Add titles', )

        parser.add_argument('--add_reviews',
                            action='store_true',
                            help='Add reviews', )

        parser.add_argument('--add_comments',
                            action='store_true',
                            help='Add comments', )

        parser.add_argument('--all',
                            action='store_true',
                            help='Create all initial data',
                            )

    @staticmethod
    def get_data(file_name):
        file_path = finders.find(f'data/{file_name}')
        with open(file_path, 'r', encoding="utf-8") as file:
            data_reader = csv.DictReader(file)
            data = []
            for row in data_reader:
                for key, value in row.items():
                    if value.isdigit():
                        row[key] = int(value)
                data.append(row)
        return data

    @staticmethod
    def create_objects(model, data):
        for el in data:
            try:
                model.objects.create(**el)
            except Exception as e:
                print(f'Unable to create an object {model.__class__.__name__} '
                      f'with parameters: {el}, error: {e}')

    def handle(self, *args, **options):
        if options['all'] or options['add_users']:
            users = self.get_data('users.csv')
            self.create_objects(User, users)

        if options['all'] or options['add_category']:
            categories = self.get_data('category.csv')
            self.create_objects(Category, categories)

        if options['all'] or options['add_gener']:
            genres = self.get_data('genre.csv')
            self.create_objects(Gener, genres)

        if options['all'] or options['add_titles']:
            titles = self.get_data('titles.csv')
            gener_titles = self.get_data('genre_title.csv')
            # for el in gener_titles:
            #     try:
            #         title = Title.objects.get(id=el['title_id'])
            #         title.genre.add(el['genre_id'])
            #     except Exception as e:
            #         print(f'Failed to add genre to title, error: {e}')

        # if options['all'] or options['add_reviews']:
        #     reviews = self.get_data('review.csv')
        #     self.create_object(Reviews, reviews)

        # if options['all'] or options['add_comments']:
        #     comments = self.get_data('comments.csv')
        #     self.create_object(Comments, comments)
