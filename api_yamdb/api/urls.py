from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'users', views.UserModelViewSet)
router.register('categories', views.CategoryViewSet)
router.register('genres', views.GenerViewSet)
router.register('titles', views.TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments'
)

app_name = 'api_v1'


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.create_user, name='create_user'),
    path('v1/auth/token/', views.get_token, name='get_token')
]
