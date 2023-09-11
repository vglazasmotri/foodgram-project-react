from rest_framework import routers
from django.urls import include, path

from api.views import (
    index, CustomUserViewSet, IngredientViewSet, RecipeViewSet, TagViewSet,
)

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('users', CustomUserViewSet, basename='users')



urlpatterns = [
    path('index/', index),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]