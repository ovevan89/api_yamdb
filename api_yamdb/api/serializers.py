from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from review.models import (User, Category, Gener, Title, Review, Comment)


class UserSerializer(serializers.ModelSerializer):
    """Общий сериализатор для модели User."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Создаем сериализатор регистрации юзеров и отправки секретного кода."""
    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    """Создаем кастомный сериализатор с нужными полями для получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gener
        fields = "__all__"
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    # todo преопределить поля категории и жанра
    category = SlugRelatedField(
        read_only=True,
        slug_field='slug'
    )
    genre = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(title=title, author=user).exists():
            raise serializers.ValidationError(
                'Нельзя написать больше одного отзыва'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        medel = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')
