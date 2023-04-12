from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'users', views.UserModelViewSet)
router.register('categories', views.CategoryViewSet)
router.register('genres', views.GenerViewSet)


app_name = 'api_v1'


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.create_user, name='create_user'),
    path('v1/auth/token/', views.get_token, name='get_token')
]
