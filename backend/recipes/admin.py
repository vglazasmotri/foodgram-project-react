from django.contrib import admin

from recipes.models import (
    Tag, Recipe, Ingredient, RecipeIngredient, Cart, Follow, Favorite,
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites', 'pub_date')
    list_filter = ('name', 'author', 'tags')
    inlines = (RecipeIngredientInline, )

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = (
        'Добавлений в избранное'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
