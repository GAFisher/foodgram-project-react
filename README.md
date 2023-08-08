# praktikum_new_diplom

## Описание
FoodGram - дипломная работа курса backend-разработки на python Яндекс Практикум. 
Сервис служит для обмена рецептами и их публикации. 
После регистрации и авторизации, пользователь может подписаться на понравившихся авторов, составлять список избранных рецептов, загружать или составлять список покупок. 
Неавторизованные пользователи могут просто просматривать рецепты. 

## Установка
Установка использует docker, поэтому детально будет описана во 2 части сдачи проекта


## Примеры использования

По  GET запросу 
```
http://127.0.0.1:8000/api/recipes/
```

получаем список рецептов:
```
{
    "count": 10,
    "next": "http://127.0.0.1:8000/api/recipes/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "tags": [
                {
                    "id": 1,
                    "name": "Завтрак",
                    "color": "#fcf2ec",
                    "slug": "breakfast"
                }
            ],
            "author": {
                "email": "g.fisher@yandex.ru",
                "id": 3,
                "username": "g.fisher",
                "first_name": "Галина",
                "last_name": "Фишер",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 15327,
                    "name": "яйцо",
                    "measurement_unit": "шт.",
                    "amount": 2
                },
                {
                    "id": 1032,
                    "name": "молоко",
                    "measurement_unit": "г",
                    "amount": 200
                },
                {
                    "id": 15326,
                    "name": "тосты",
                    "measurement_unit": "шт.",
                    "amount": 4
                },
                {
                    "id": 1547,
                    "name": "сахар",
                    "measurement_unit": "г",
                    "amount": 25
                },
                {
                    "id": 2171,
                    "name": "ягоды",
                    "measurement_unit": "г",
                    "amount": 100
                },
                {
                    "id": 15328,
                    "name": "сироп топинамбура",
                    "measurement_unit": "ст. л.",
                    "amount": 3
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Французские тосты",
            "image": "http://127.0.0.1:8000/media/recipes/2023-05-01_15.21.53_Pq7gjD1.jpg",
            "text": "Смешать молоко с сахаром, добавить яйца, тщательно все взбить. Обмакнуть тосты в смесь и жарить на сливочном масле до золотистой корочки. Полить сверху сиропом топинамбура и украсить ягодами.",
            "cooking_time": "20"
        },
...
```

## Автор

[Galina Fisher](https://github.com/GAFisher)