# API для Yatube

## Описание

REST API для социальной сети Yatube.

API позволяет:
- создавать, редактировать и удалять посты;
- добавлять и удалять комментарии;
- получать список групп;
- подписываться на авторов;
- работать с JWT-аутентификацией.

---

## Технологии

- Python 3.10
- Django
- Django REST Framework
- Simple JWT

---

## Установка

Клонировать репозиторий:

git clone <ссылка_на_репозиторий>

Перейти в папку проекта:

cd api-final-yatube

Создать виртуальное окружение:

python -m venv venv

Активировать виртуальное окружение:

Windows:
venv\Scripts\activate

Linux/macOS:
source venv/bin/activate

Установить зависимости:

pip install -r requirements.txt

Применить миграции:

python manage.py migrate

Запустить сервер:

python manage.py runserver

---

## Получение JWT-токена

Создание токена:

POST /api/v1/jwt/create/

Тело запроса:

{
  "username": "username",
  "password": "password"
}

Обновление токена:

POST /api/v1/jwt/refresh/

Проверка токена:

POST /api/v1/jwt/verify/

---

## Примеры запросов

Получить список постов:

GET /api/v1/posts/

Создать пост:

POST /api/v1/posts/

{
  "text": "Новый пост"
}

Получить комментарии к посту:

GET /api/v1/posts/{post_id}/comments/

Подписаться на пользователя:

POST /api/v1/follow/

{
  "following": "username"
}

Получить список своих подписок:

GET /api/v1/follow/

---

## Автор

Учебный проект Яндекс Практикум.