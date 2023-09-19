from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    """Тег."""
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    """Рецепт."""
    name = models.CharField(max_length=200)
    image = models.ImageField(
        verbose_name='Изображение рецепта',
        upload_to='recipes/')
    cooking_time = models.PositiveIntegerField()
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')
    
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'))
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']


class Ingredient(models.Model):
    """Ингредиент."""
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeIngredient(models.Model):
    """Колличество ингредиента в рецепте."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()


class Follow(models.Model):
    """Подписка."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'
        ordering = ['-author']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='can_not_follow_yourself'
            ),
        ]

    def __str__(self):
        return f'{self.user} subscribed on {self.author}'


class Cart(models.Model):
    """Корзина покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shoppingcart'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class Favorite(models.Model):
    """Избранное."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'
