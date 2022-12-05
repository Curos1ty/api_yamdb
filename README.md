# api_yamdb
api_yamdb
### Описание
API YAMDB имеет следующие ресурсы: 
Описание (адрес по умолчанию http://127.0.0.1:8000/api/v1/) | Какие методы запросов настроены
---------|--------
Категории: categories/, categories/{slug}/ | GET(list), POST, DELETE
Жанры: genres/, genres/{slug}/ | GET(list), POST, DELETE
Произведения: titles/, titles/{titles_id}/ | GET(list), POST, GET(retrieve), PATCH, DELETE
Отзывы: titles/{title_id}/reviews/, titles/{title_id}/reviews/{review_id}/ | GET(list), POST, GET(retrieve), PATCH, DELETE
Комментарии: titles/{title_id}/reviews/{review_id}/comments/, {title_id}/reviews/{review_id}/comments/{comment_id}/ | GET(list), POST, GET(retrieve), PATCH, DELETE
Пользователи: users/, users/{username}/, | GET(list), POST, GET(retrieve) user, PATCH, DELETE, GET (me), PATCH(me)
### Технологии
* Python 3.7.9 64-bit
* Django 2.2.16
* sqlparse 0.4.3
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение

Описание | Команда в терминале
---------|--------
Установка виртуального окружения из корневой папки проекта | python3 -m venv venv
Активация виртуального окружения | source/venv/bin/activate
В виртуальном окружении установите зависимости | pip install -r requirements.txt
Выполните миграции | python3 manage.py migrate

Для загрузки данных из файлов csv в базу данных поочередно запустить команды:

```
python manage.py import_category_csv

python manage.py import_genre_csv

python manage.py import_titles_csv

python manage.py import_genretitle_csv

python manage.py import_users_csv

python manage.py import_review_csv

python manage.py import_comments_csv
```

- Запустите django server для проекта

Описание | Команда в терминале
---------|--------
Используя виртуальное окружение запустите сервер из корневой папки проекта где есть файл manage.py | python3 manage.py runserver

Перейдите по адресу: http://127.0.0.1:8000/api/v1/ и наслаждайтесь.

### Примеры запросов

##### Добавление новой категории. Права доступа: Администратор

Запрос POST http://127.0.0.1:8000/api/v1/categories/
Request samples:
```json
{
    "name": "string",
    "slug": "string",
}
```

* name (required) string (наименование категории)
* slug (required) string (название для ссылки)

Вывод (Response samples):
``` json
{
    "name": "string",
    "slug": "string"
}
```

##### Добавление нового отзыва.

Запрос POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
Request samples:
```json
{
    "text": "string"
    "score": 1
}
```

* text (required) string
* score (required) integer

Вывод (Response samples):
``` json
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
```
Подробнее о запросах и примерах можно узнать по адресу http://127.0.0.1:8000/redoc/
### Вы восхитительны!

### Авторы
Ирина Елисеева - модели, view, эндпоинты для произведений, категорий, жанров, реализация импорта данных из csv файлов.
Юсуп Шарафутдинов - работает над: отзывами, комментариями, рейтингом произведений.
Михаил Передереев - вся часть, касющаяся управлением пользователей: система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения через e-mail 