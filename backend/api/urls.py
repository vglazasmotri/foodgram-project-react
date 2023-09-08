from rest_framework import routers
from django.urls import include, path

from api.views import (
    index, CustomUserViewSet, IngredientViewSet, RecipeViewSet, TagViewSet,
)

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('users', CustomUserViewSet)



urlpatterns = [
    path('index/', index),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]