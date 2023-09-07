from django.shortcuts import render, HttpResponse
from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet

from recipes.models import Tag, Recipe
from api.serializers import (
    TagSerializer, RecipeSerializer, RecipeCreateSerializer, 
    CustomUserSerializer,
    )

from users.models import User

def index(request):
    return HttpResponse('index')

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'recipeingredient_set__ingredient', 'tags'
        ).all()
        return recipes

    # def get_serializer(self):
    #     # Добавить для других типов запросов
    #     if self.action == 'create':
    #         return RecipeCreateSerializer
    #     return RecipeSerializer
    
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)