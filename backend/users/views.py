from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User, Subscription
from .serializers import SubscriptionSerializer
from recipes.pagination import CustomPagination


class CustomUserViewSet(UserViewSet):
    """Вьюсет для работы с пользователями."""

    def get_permissions(self):
        if self.action == 'me':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        """Метод для возвращения подпискок пользователя."""
        user = request.user
        subscriptions = user.subscriber.all()
        subscribed_users = [
            subscription.author for subscription in subscriptions
        ]
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(subscribed_users, request)
        serializer = SubscriptionSerializer(
            result_page, many=True, context={'request': request}
        )
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id=None):
        """Метод для создания/удаления подписки на автора."""
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if author == request.user:
                return Response(
                    {'errors': 'Нельзя подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if Subscription.objects.filter(
                    user=request.user, author=author
            ).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на этого автора.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Subscription.objects.create(user=request.user, author=author)
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Subscription.objects.filter(
                    user=request.user, author=author
            ).exists():
                return Response(
                    {
                        'errors': 'Подписка не была оформлена, либо удалена.'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Subscription.objects.filter(
                user=request.user, author=author
            ).delete()
            return Response(
                {'message': 'Подписка удалена.'},
                status=status.HTTP_204_NO_CONTENT,
            )
