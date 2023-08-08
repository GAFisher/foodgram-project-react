from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from .models import User, Subscription
from recipes.models import Recipe


class CustomUserSerializer(UserSerializer):
    """Сериализатор для просмотра пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        """Метод для проверки подписан ли текущий пользователь на этого."""
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, author=obj).exists()
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password')


class ShortlistRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецептов в подписках."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(UserSerializer):
    """Сериализатор для подписок пользователя."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = ShortlistRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
            'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """Метод для проверки подписан ли текущий пользователь на этого."""
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, author=obj).exists()
        return False


    def get_recipes_count(self, obj):
        """Метод для получения общего количества рецептов пользователя."""
        return obj.recipes.count()
