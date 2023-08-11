# Проект «Продуктовый помощник»

## Описание
FoodGram - дипломная работа курса backend-разработки на python Яндекс Практикум. 
Сервис служит для обмена рецептами и их публикации. 
После регистрации и авторизации, пользователь может подписаться на понравившихся авторов, составлять список избранных рецептов, загружать или составлять список покупок. 
Неавторизованные пользователи могут просто просматривать рецепты. 

Тестовый сервер: `flavorfinder.sytes.net`. Логин: `admin`. Пароль:`Admin123`

## Как запустить проект
1. Клонируйте репозиторий.
2. Создайте и активируйте виртуальное окружение:
```
python3 -m venv venv
source venv/bin/activate
```
3. Создайте файл .env с переменными окружения внутри директории `foodgram` со следующим содержимым:
```
SECRET_KEY=<Cекретный ключ из файла settings.py>
DB_ENGINE=<Указываем, что работаем с postgresql>
POSTGRES_USER=<Логин для подключения к базе данных>
POSTGRES_PASSWORD=<Пароль для подключения к БД>
POSTGRES_DB=<Имя базы данных>
DB_HOST=<Название сервиса (контейнера)>
DB_PORT=<Порт для подключения к БД>
```
4. Запустите docker-compose командой `docker-compose up -d --build`.
5. Выполните по очереди команды:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
- Выполните команду для заполнения базы данными:
```
sudo docker compose exec backend python manage.py import_csv
```
- Создайте суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```
- Выполните команду для сбора статических файлов:
```
sudo docker compose exec backend manage.py collectstatic --no-input
```
- Создайте дамп (резервную копию) базы:
```
sudo docker compose exec backend python manage.py dumpdata > fixtures.json 
```
Проект будет доступен по адресам:
- Главная страница: `http://<ip-адрес>/`
- Документация проекта: `http://<ip-адрес>/api/docs/`
- API проекта: `http://<ip-адрес>/api/`
- Admin-зона: `http://<ip-адрес>/admin/`

Теги вручную добавляются в админ-зоне в модель Tags.

## Регистрация новых пользователей
1. Пользователь отправляет POST-запрос с параметрами `email`, `username`, `first_name`, `last_name` и `password` на эндпоинт `/api/users/`:
```
{
    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "password": "Qwerty123!"
}
```
2. Пользователь отправляет POST-запрос с параметрами `email` и `password` на эндпоинт `/api/auth/token/login/`, в ответе на запрос ему приходит токен авторизации:
```
{
    "email": "vpupkin@yandex.ru",
    "password": "Qwerty123!"
}
```
Пример ответа:
```
{
    "auth_token": "0c2e40ef07b3e7d9a4fa03b22b90acd68192cd50"
}
```



## Примеры использования

### Получить список рецептов:
Отправьте GET-запрос на эндпоинт `/api/recipes/`. Пример ответа:
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
                "email": "vpupkin@yandex.ru",
                "id": 1,
                "username": "vasya.pupkin",
                "first_name": "Вася",
                "last_name": "Пупкин",
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
### Добавление нового рецепта:
Отправьте POST-запрос на эндпоинт `/api/recipes/`, передав:
* Список ингредиентов: `ingredients`
* Список id тегов: `tags`
* Картинку, закодированную в Base64: `image`
* Название рецепта: `name`
* Описание рецепта: `text`
* Время приготовления (в минутах): `cooking_time`

```
{
    "ingredients": [
        {
            "id": 2190,
            "amount": 6
        },
        {
            "id": 1647,
            "amount": 10
        },
        {
            "id": 1123,
            "amount": 10
        }                  
    ],
        "tags": [
            1,
            2,
            3
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "Омлет в духовке",
    "text": "В глубокую миску вбиваем яйца, вливаем молоко, добавляем немного соли и перемешиваем все ингредиенты. Вливаем основу для омлета в форму, смазанную сливочным маслом, и отправляем в духовку.",
    "cooking_time": 40
}
```
Пример ответа:
```
{
    "id": 2,
    "tags": [
        {
            "id": 1,
            "name": "Завтрак",
            "color": "#e26c2d",
            "slug": "breakfast"
        },
        {
            "id": 2,
            "name": "Обед",
            "color": "#49b64e",
            "slug": "lunch"
        },
        {
            "id": 3,
            "name": "Ужин",
            "color": "#8775d2",
            "slug": "dinner"
        }
    ],
    "author": {
        "email": "vpupkin@yandex.ru",
        "id": 1,
        "username": "vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
    },
    "ingredients": [
        {
            "id": 2190,
            "name": "яйцо",
            "measurement_unit": "шт.",
            "amount": 6
        },
        {
            "id": 1647,
            "name": "сливочное масло",
            "measurement_unit": "г",
            "amount": 10
        },
        {
            "id": 1032,
            "name": "молоко",
            "measurement_unit": "г",
            "amount": 300
        }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "name": "Омлет в духовке",
    "image": "http://127.0.0.1:8000/media/recipes/temp.png",
    "text": "В глубокую миску вбиваем яйца, вливаем молоко, добавляем немного соли и перемешиваем все ингредиенты. Вливаем основу для омлета в форму, смазанную сливочным маслом, и отправляем в духовку.",
    "cooking_time": "40"
}
```
## Автор

[Галина Фишер](https://github.com/GAFisher), студент когорты 21+ Яндекс.Практикум