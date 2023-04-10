from rest_framework import viewsets
from review.models import User
from api import serializers
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status, pagination, permissions
from rest_framework_simplejwt.tokens import AccessToken


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_user(request):
    """Создаем пользователя. Код для получения токена отправляется на почту."""
    serializer = serializers.UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = get_object_or_404(User, username=serializer.validated_data['username'])
        email = serializer.validated_data['email']
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Регистрация в сервисе Yamdb',
            f'Your code is here {confirmation_code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Сверяем код подтверждения и получаем токен доступа."""
    serializer = serializers.TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=serializer.validated_data['username'])
        confirmation_code = serializer.validated_data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


