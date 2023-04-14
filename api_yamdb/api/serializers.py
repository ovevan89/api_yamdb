from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from review.models import Category, Gener, Title, User


class UserSerializer(serializers.ModelSerializer):
    """Общий сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для endpoint 'me'. """

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Создаем сериализатор регистрации юзеров и отправки секретного кода."""

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value.lower() == "me" or User.objects.filter(username='me'):
            raise ValidationError("Username 'me' is not valid")
        return value


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
    # todo переопределить поля категории и жанра
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
