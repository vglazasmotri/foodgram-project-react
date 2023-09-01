from rest_framework import routers
from django.urls import include, path

from api.views import index, CustomUserViewSet, TagViewSet, RecipeViewSet

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('index/', index),
    # path('/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]