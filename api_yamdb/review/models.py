import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models


class User(AbstractUser):
    ROLES = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        validators=[
            RegexValidator(
                r'^[\w.@+-]+\Z',
                'Поле "username" не соответствует формату.',
                'invalid'
            )
        ],
        unique=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )

    bio = models.TextField(
        verbose_name='О себе', blank=True, null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default='user'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='username cant be is me'
            )
        ]

    def is_administrator(self):
        return self.is_superuser or self.role == 'admin'

    def is_moderator(self):
        return self.role == 'moderator'


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(datetime.date.today().year)]
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.name} - {self.year}'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
