from rest_framework import serializers
from review.models import User


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
