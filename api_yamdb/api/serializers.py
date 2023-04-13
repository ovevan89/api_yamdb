from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Title, User, Review, Comment, Genre


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
        if value.lower() == "me":
            raise ValidationError("Username 'me' is not valid")
        return value


class TokenSerializer(serializers.Serializer):
    """Создаем кастомный сериализатор с нужными полями для получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitlePostSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"
        extra_kwargs = {
            'genre': {'required': True},
            'category': {'required': True}
        }

    def get_rating(self, obj):
        result = obj.reviews.aggregate(avg=Avg('score')).get('avg', None)
        return result


class TitleGetSerializer(TitlePostSerializer):
    category = CategorySerializer()
    genre = GenerSerializer(many=True)

    class Meta:
        model = Title
        fields = "__all__"
        read_only_fields = ('__all__',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
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
    """Comment serializer."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
