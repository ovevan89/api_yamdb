from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from review.models import (User, Category, Gener, Title)


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
    # todo добавить поле рейтинг
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Gener.objects.all()
    )
    # rating =

    class Meta:
        model = Title
        fields = "__all__"
        extra_kwargs = {
            'genre': {'required': True},
            'category': {'required': True}
        }
