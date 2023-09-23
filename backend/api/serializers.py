from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    Tag, Recipe, RecipeIngredient, Follow, Favorite, Cart, Ingredient,
)
from users.models import User


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Cart."""
    class Meta:
        model = Cart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже в списоке покупок.',
            )
        ]


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


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""
    class Meta:
        model = Tag
        fields = '__all__'


class CustomUserSerializer(UserSerializer):
    """Отображение пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """
        Возвращает True если автор в Подписках у юзера
        и False в остальных случаях.
        """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class CustomCreateUserSerializer(UserCreateSerializer):
    """Создание пользователя."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиентов в рецептах."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов в рецепты."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для короткого отображения рецептов."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецептов."""
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipeingredient_set',
    )
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


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения рецептов."""
    ingredients = RecipeIngredientCreateSerializer(many=True)
    image = Base64ImageField(use_url=True, max_length=None)

    class Meta:
        model = Recipe
        fields = (
            'name', 'image', 'cooking_time', 'text', 'tags', 'ingredients',
        )

    def to_representation(self, instance):
        """
        В случае удачного добавления или изменения рецепта меняет сериализатор.
        """
        serializer = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )
        return serializer.data

    @staticmethod
    def add_ingredients(ingredients, instance):
        """Добавляет ингредиенты в рецепт."""
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                ingredient=ingredient_data['ingredient'],
                recipe=instance,
                amount=ingredient_data['amount']
            )
            for ingredient_data in ingredients
        ])

    def validate_ingredients(self, ingredients):
        """Проверяем ингредиенты при создании и редактировании рецепта."""
        list_ingredients = [
            ingredient.get('id') for ingredient in ingredients
        ]
        if not list_ingredients:
            raise serializers.ValidationError(
                "Нужно добавить хотябы 1 ингредиент."
            )
        elif len(list_ingredients) != len(set(list_ingredients)):
            raise serializers.ValidationError(
                'Ингредиенты в рецепте не должны повторятся.'
            )
        for ingredient in ingredients:
            if int(ingredient.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента не может быть меньше 1.'
                )
        return ingredients

    def create(self, validated_data):
        """ОСоздание рецепта."""
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)
        self.add_ingredients(ingredients, instance)
        return instance

    def update(self, instance, validated_data):
        """Обновление рецепта."""
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time,
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
                'Нельзя подписаться на самого себя!',
            )
        return data


class SubscriptionShowSerializer(CustomUserSerializer):
    """Отображение списока подписок на авторов."""
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
        """Список рецептов для карточки автора на странице подписок."""
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        author_recipes = object.recipes.all()
        if limit:
            author_recipes = author_recipes[:int(limit)]
        return RecipeShortSerializer(author_recipes, many=True).data

    def get_recipes_count(self, object):
        return object.recipes.count()
