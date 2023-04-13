from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api import serializers
from api.permissions import AdminOrReadOnly, IsAdmin, OwnerOrReadOnly
from api.filters import TitleFilter
from api.permissions import AdminOrReadOnly, IsAdmin
from api.serializers import (CategorySerializer, GenerSerializer,
                             TitleSerializer, ReviewSerializer,
                             CommentSerializer)
from review.models import Category, Genre, Title, User, Review, Comment
                             TitlePostSerializer, TitleGetSerializer)
from review.models import Category, Genre, Title, User
from utils.function import send_user_email


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdmin]
    http_method_names = ['list', 'post', 'get', 'patch', 'delete']
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'],
            serializer_class=serializers.UserProfileSerializer,
            url_path='me',
            permission_classes=[permissions.IsAuthenticated]
            )
    def get_user_profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_user(request):
    """Создаем пользователя. Код для получения токена отправляется на почту."""
    serializer = serializers.UserRegistrationSerializer(data=request.data)
    username = request.data.get('username')
    email = request.data.get('email')
    if User.objects.filter(username=username, email=email).exists():
        send_user_email(request.data['username'], email=request.data['email'])
    else:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_user_email(request.data['username'], email=request.data['email'])
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'detail': 'Письмо отправлено'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Сверяем код подтверждения и получаем токен доступа."""
    serializer = serializers.TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        confirmation_code = serializer.validated_data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    model = Category
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class GenerViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    model = Genre
    serializer_class = GenerSerializer
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class TitleViewSet(ModelViewSet):
    model = Title
    serializer_class = TitlePostSerializer
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filterset_class = TitleFilter
    # filter_backends = [filters.SearchFilter]
    # search_fields = ('name', 'year', 'category__slug', 'genre__slug')
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        """Список комментариев под определёным отзывом."""
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title_id=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        """Добавление комментария к отзыву."""
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title_id=title_id)
        serializer.save(author=self.request.user, review=review)