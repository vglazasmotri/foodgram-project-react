from django.shortcuts import render, HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import permissions, status
from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action

from rest_framework.pagination import PageNumberPagination

from recipes.models import Tag, Recipe, Ingredient, Follow, Favorite, Cart
from api.serializers import (
    IngredientSerializer, TagSerializer, RecipeSerializer,
    CustomUserSerializer, SubscriptionSerializer, SubscriptionShowSerializer,
    FavoriteSerializer, RecipeShortSerializer, RecipeCreateSerializer,
    CartSerializer,
    )

from users.models import User
from .filters import IngredientFilter, RecipeFilter
from .permissions import AuthorOrReadOnly

def index(request):
    return HttpResponse('index')

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AuthorOrReadOnly,)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='subscribe',
        url_name='subscribe',
    )
    def get_subscribe(self, request, id):
        """Подписаться и отписываться от авторарецепта."""
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                data={'user': request.user.id, 'author': author.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            author_serializer = SubscriptionShowSerializer(
                author, context={'request': request}
            )
            return Response(
                author_serializer.data, status=status.HTTP_201_CREATED
            )
        subscription = get_object_or_404(
            Follow, user=request.user, author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions',
        url_name='subscriptions',
    )
    def get_subscriptions(self, request):
        """Список авторов на которых подписан."""
        authors = User.objects.filter(following__user=request.user)
        paginator = PageNumberPagination()
        result_pages = paginator.paginate_queryset(
            queryset=authors, request=request
        )
        serializer = SubscriptionShowSerializer(
            result_pages, context={'request': request}, many=True
        )
        return paginator.get_paginated_response(serializer.data)
    
class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    search_fields = ('^name', )
    pagination_class = None

class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
        url_name='favorite',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_favorite(self, request, pk):
        """Позволяет текущему пользователю добавлять рецепты в избранное."""
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data={'user': request.user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            favorite_serializer = RecipeShortSerializer(recipe)
            return Response(
                favorite_serializer.data, status=status.HTTP_201_CREATED
            )
        favorite_recipe = get_object_or_404(
            Favorite, user=request.user, recipe=recipe
        )
        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_shopping_cart(self, request, pk):
        """Позволяет текущему пользователю добавлять рецепты
        в список покупок."""
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = CartSerializer(
                data={'user': request.user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            shopping_cart_serializer = RecipeShortSerializer(recipe)
            return Response(
                shopping_cart_serializer.data, status=status.HTTP_201_CREATED
            )
        shopping_cart_recipe = get_object_or_404(
            Cart, user=request.user, recipe=recipe
        )
        shopping_cart_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'recipeingredient_set__ingredient', 'tags'
        ).all()
        return recipes

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)