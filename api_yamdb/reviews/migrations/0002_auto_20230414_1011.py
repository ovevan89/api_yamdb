# Generated by Django 3.2 on 2023-04-14 07:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'genre'},
        ),
        migrations.AlterModelOptions(
            name='genretitle',
            options={'verbose_name': 'gener_title'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'verbose_name': 'title'},
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(db_index=True, validators=[django.core.validators.MaxValueValidator(2023)]),
        ),
        migrations.AlterModelTable(
            name='category',
            table='tbl_category',
        ),
        migrations.AlterModelTable(
            name='genre',
            table='tbl_genre',
        ),
        migrations.AlterModelTable(
            name='genretitle',
            table='tbl_gener_title',
        ),
        migrations.AlterModelTable(
            name='title',
            table='tbl_title',
        ),
    ]