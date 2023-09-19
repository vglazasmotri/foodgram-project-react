from django.contrib import admin

from recipes.models import (
    Tag, Recipe, Ingredient, RecipeIngredient, Cart, Follow, Favorite,
)

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'count_favorites', 'pub_date',
    )
    list_filter = ('name', 'author', 'tags')
    inlines = (RecipeIngredientInline, )

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = (
        'Добавлений в избранное'
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass