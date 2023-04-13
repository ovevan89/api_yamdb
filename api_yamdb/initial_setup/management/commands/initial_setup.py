import csv
import logging

from django.contrib.staticfiles import finders

from django.core.management import BaseCommand

from review.models import User, Category, Genre, Title, GenreTitle

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

        parser.add_argument('--add_genre',
                            action='store_true',
                            help='Add genres', )

        parser.add_argument('--add_titles',
                            action='store_true',
                            help='Add titles', )

        parser.add_argument('--add_genre_title',
                            action='store_true',
                            help='Add genre_title', )

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
    def get_data(model, file_name):
        _replacing_fields = {
            Title: {
                'category': 'category_id'
            },
            GenreTitle: {
                'title': 'title_id',
                'genre': 'genre_id'
            }
            # Reviews: {
            #     'author': 'author_id',
            #     'title': 'title_id'
            # },
            # Comments: {
            #     'author': 'author_id',
            #     'review': 'review_id'
            # }
        }

        file_path = finders.find(f'data/{file_name}')
        with open(file_path, 'r', encoding="utf-8") as file:
            data_reader = csv.DictReader(file)
            data = []
            for row in data_reader:
                if model in _replacing_fields:
                    model_dict = _replacing_fields[model]
                    for key in model_dict.keys():
                        if key in row:
                            row[model_dict[key]] = row[key]
                            row.pop(key)
                data.append(row)
        return data

    def create_objects(self, model, file_name):
        data = self.get_data(model, file_name)
        for el in data:
            try:
                obj = model.objects.create(**el)
                print(f'Object {model.__name__} was created with id {obj.id}')

            except Exception as e:
                print(f'Unable to create an object {model.__name__} '
                      f'with parameters: {el}, error: {e}')

    def handle(self, *args, **options):
        if options['all'] or options['add_users']:
            self.create_objects(User, 'users.csv')

        if options['all'] or options['add_category']:
            self.create_objects(Category, 'category.csv')

        if options['all'] or options['add_genre']:
            self.create_objects(Genre, 'genre.csv')

        if options['all'] or options['add_titles']:
            self.create_objects(Title, 'titles.csv')

        if options['all'] or options['add_genre_title']:
            self.create_objects(GenreTitle, 'genre_title.csv')

        # if options['all'] or options['add_reviews']:
        #     self.create_object(Reviews, 'review.csv')

        # if options['all'] or options['add_comments']:
        #     self.create_object(Comments, 'comments.csv')
