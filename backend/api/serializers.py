from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Tag, Recipe, RecipeIngredient, Follow, Favorite, Cart, Ingredient
from users.models import User
from djoser.serializers import UserCreateSerializer, UserSerializer

RECIPES_LIMIT = 6

# Сериализаторы Список покупок
class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже в списоке покупок.'
            )
        ]

# Сериализаторы Избранное
class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Favorite."""

    class Meta:
        model = Favorite
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Этот рецепт уже в избраном.'
            )
        ]

# Сериализаторы Ингредиент
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

# Сериализаторы Тега
class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

# Сериализаторы Пользователя Чтение
class CustomUserSerializer(UserSerializer):
    """Получение списка пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        """
        Возвращает True если автор в Подписках у юзера
        и False в остальных случаях.
        """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()

# Сериализаторы Пользователя Создание
class CustomCreateUserSerializer(UserCreateSerializer):
    """Регистация нового пользователя."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

# Сериализаторы Ингредиент-Рецепт Чтение
class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

# Сериализаторы Ингредиент-Рецепт Создание
class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')

# Сериализаторы Рецепта коротко Чтение
class RecipeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )

# Сериализаторы Рецепта Чтение
class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredient_set')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()


    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        """
        Возвращает True если рецепт в Избанном у юзера
        и False в остальных случаях.
        """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        """
        Возвращает True если рецепт в Корзине юзера
        и False в остальных случаях.
        """

        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Cart.objects.filter(
            user=request.user, recipe=obj
        ).exists()

# Сериализаторы Рецепта Создание
class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(many=True)
    image = Base64ImageField(use_url=True, max_length=None)

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'cooking_time', 'text', 'tags', 'ingredients')
        
    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )
        return serializer.data
    
    @staticmethod
    def add_ingredients(ingredients, instance):
        """Добавляет ингредиенты."""
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                ingredient=ingredient_data['ingredient'],
                recipe=instance,
                amount=ingredient_data['amount']
            )
            for ingredient_data in ingredients
        ])

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)
        self.add_ingredients(ingredients, instance)
        return instance

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.tags.clear()
        instance.ingredients.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.add(*tags)
        recipe = instance
        self.add_ingredients(ingredients, recipe)
        instance.save()
        return instance

# Сериализаторы Подписок Создание
class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Подписок."""

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписывались на этого автора.',
            ),
        ]

    def validate(self, data):
        """Если совпадают имя пользователя и автора выдает ошибку."""
        if data['user'] == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return data

# Сериализаторы Подписок Чтение
class SubscriptionShowSerializer(CustomUserSerializer):
    """Список подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, object):
        author_recipes = object.recipes.all()[:RECIPES_LIMIT]
        return RecipeShortSerializer(
            author_recipes, many=True
        ).data

    def get_recipes_count(self, object):
        return object.recipes.count()