from rest_framework import serializers

from recipes.models import Tag, Recipe, RecipeIngredient
from users.models import User
from djoser.serializers import UserCreateSerializer, UserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredient_set')
    
    class Meta:
        model = Recipe
        fields = '__all__'

class RecipeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'text', 'tags')


class CustomUserSerializer(UserCreateSerializer):
    """Сериализатор для модели User."""

    class Meta:
        """Мета-параметры сериализатора"""

        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class CustomCreateUserSerializer(CustomUserSerializer):
    """Сериализатор для создания пользователя
    без проверки на подписку """

    class Meta:
        """Мета-параметры сериализатора"""

        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

