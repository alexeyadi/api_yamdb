# Спринт 10 - Проект YaMDb (групповой проект). 
## Описание проекта:
API для отзывов и комментариев на произведения, в котором доступны следующие функции:
* создание пользователя
* получение, добавление и удаление категории (вывод с пагинацией)
* получение, добавление и удаление жанра (вывод с пагинацией)
* получение, создание, обновление, частичное обновление, удаление произведения (редактирование доступно только автору, модератору и администратору)
* получение, создание, обновление, частичное обновление, удаление отзывов на произведение (редактирование доступно только автору, модератору и администратору)
* получение, добавление, обновление, частичное обновление, удаление комментариев на отзывы (редактирование доступно только автору, модератору и администратору)

## Стек технологий используемый в проекте:
* Python - 3.7

```
https://www.python.org/
```

* Django  - 2.2.19

```
https://www.djangoproject.com/
```

* Django Rest Framework - 3.12.4

```
https://www.django-rest-framework.org/
```

* Simple JWT - 5.2.2

```
https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
```

* Django Filter - 21.1

```
https://www.django-rest-framework.org/api-guide/filtering/#setting-filter-backends
```

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/alexeyadi/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры работы с API
###### Подробная документация доступна по адресу http://127.0.0.1:8000/redoc/

## Пользовательские роли и права доступа

* Аноним — может просматривать описания произведений, читать отзывы и комментарии.
* Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
* Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
* Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
* Суперюзер Django — должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора.

### Самостоятельная регистрация новых пользователей

* Пользователь отправляет POST-запрос

```
POST /api/v1/auth/signup/
```

```json
{
  "email": "string",
  "username": "string"
}
```

* Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email
* Пользователь отправляет POST-запрос для получения JWT токена

```
/api/v1/auth/token/
```

```json
{
  "username": "string",
  "confirmation_code": "string"
}
```
### Создание пользователя администратором

* создается admin через через админ-зону сайта или через POST-запрос на специальный эндпоинт api/v1/users/
* Пользователь самостоятельно отправляет свой email и username на эндпоинт /api/v1/auth/signup/ , в ответ ему приходит письмо с кодом подтверждения.
* Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответ ему приходит token (JWT-токен), как и при самостоятельной регистрации.

### Работа с пользователями

Получение списка всех пользователей:

```
Права доступа: Администратор
GET /api/v1/users/ 
```

```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```

Добавление пользователя:

```
Права доступа: Администратор
Поля email и username должны быть уникальными.
POST /api/v1/users/
```

```json
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```

Получение пользователя по username:

```
Права доступа: Администратор
GET /api/v1/users/{username}/
```

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Изменение данных пользователя по username:

```
Права доступа: Администратор
PATCH /api/v1/users/{username}/
```

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Удаление пользователя по username:

```
Права доступа: Администратор
DELETE /api/v1/users/{username}/
```

Получение данных своей учетной записи:

```
Права доступа: Любой авторизованный пользователь
GET /api/v1/users/me/
```

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Изменение данных своей учетной записи:

```
 Права доступа: Любой авторизованный пользователь
PATCH /api/v1/users/me/
```

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```

### Примеры запросов к API для пользователя аноним
###### Для анонимных пользователей работа с API доступна в режиме только для чтения

```
Права доступа: Доступно без токена.
```
```
GET /api/v1/categories/ - Получение списка всех категорий
```
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
```
GET /api/v1/genres/ - Получение списка всех жанров
```
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
```
GET /api/v1/titles/ - Получение списка всех произведений
```
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
```
GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов
```
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
```
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву
```
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```

### Примеры запросов к API для аутентифицированных пользователей, модераторов или администраторов
### CATEGORIES
###### Категории (типы) произведений

Добавление новой категории:

```
Права доступа: Администратор.
POST /api/v1/categories/
```

```json
{
  "name": "string",
  "slug": "string"
}
```

Удаление категории:

```
Права доступа: Администратор.
DELETE /api/v1/categories/{slug}/
```

### TITLES
###### Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

Добавление произведения:

```
Права доступа: Администратор.
POST api/v1/titles/
```

```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Частичное обновление информации о произведении

```
Права доступа: Администратор
PATCH api/v1/titles/{titles_id}/
```

```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Удаление произведения:

```
DEL http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

##### Запросы к API по GENRES, REVIEWS и COMMENTS делаются аналогично, более подробно можно посмотреть по адресу http://127.0.0.1:8000/redoc/

### Авторы проекта:
- :man_technologist: [Алексей Адищев - alexeyadi (первый разработчик. Тимлид)](https://github.com/alexeyadi)
- :man_technologist: [Малышев Тимур - Helep0 (второй разработчик)](https://github.com/Helep0/)
- :woman_technologist: [Наталия Сатанцева - Nata-Sata (третий разработчик)](https://github.com/Nata-Sata)





