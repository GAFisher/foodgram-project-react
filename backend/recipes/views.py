from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Favorite,
    ShoppingCart,
)
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeListSerializer,
    RecipeCreateSerializer,
    FavoriteRecipeSerializer,
)
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnlyPermission


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с рецептами."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeCreateSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        """Метод для добавления/удаления рецепта в избранное."""
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в избранное.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = FavoriteRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Favorite.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт не добавлен в избранное.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite = get_object_or_404(
                Favorite, user=request.user, recipe=recipe
            )
            favorite.delete()
            return Response(
                {'message': 'Рецепт удалён из избранного.'},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        """Метод для добавления/удаления рецепта в список покупок."""
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в список покупок.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            serializer = FavoriteRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not ShoppingCart.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт не добавлен в список покупок.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite = get_object_or_404(
                ShoppingCart, user=request.user, recipe=recipe
            )
            favorite.delete()
            return Response(
                {'message': 'Рецепт удалён из списка покупок.'},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        """Метод для скачивания списка покупок."""
        recipes_in_shoppingcart = ShoppingCart.objects.filter(
            user=request.user
        )

        ingredient_quantities = {}
        for recipe in recipes_in_shoppingcart:
            recipe_ingredients = RecipeIngredient.objects.filter(
                recipe=recipe.recipe
            )
            for ingredient in recipe_ingredients:
                ingredient_amount = ingredient.amount
                ingredient_name = (
                    f'{ingredient.ingredient.name}'
                    f'({ingredient.ingredient.measurement_unit})'
                )
                if ingredient_name in ingredient_quantities:
                    ingredient_quantities[ingredient_name] += ingredient_amount
                else:
                    ingredient_quantities[ingredient_name] = ingredient_amount

        content = '\n'.join(
            f'{ingredient} - {amount}'
            for ingredient, amount in ingredient_quantities.items()
        )

        response = HttpResponse(content, content_type='text/plain')
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_cart.txt"'
        return response
