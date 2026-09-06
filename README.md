# Mini Forum API

Учебный REST API небольшого форума, разработанный на FastAPI.

Пользователи могут регистрироваться, входить в аккаунт, создавать темы, писать сообщения и ставить лайки. Редактировать и удалять можно только собственные темы и сообщения.

## Возможности

- Регистрация пользователей
- Авторизация через JWT
- Получение и изменение профиля
- Просмотр категорий форума
- Создание, редактирование и удаление тем
- Добавление сообщений в темы
- Редактирование и удаление своих сообщений
- Лайки сообщений
- Поиск тем по названию
- Фильтрация тем по категории и автору
- Пагинация тем и сообщений

## Технологии

- Python 3.12+
- FastAPI
- Pydantic
- SQLAlchemy 2.0 Async
- PostgreSQL
- asyncpg
- Alembic
- PyJWT
- pwdlib
- Uvicorn
- Pytest
- Git и GitHub

## Структура проекта

```text
mini-forum/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── database.py
│   ├── models/
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── topic.py
│   │   ├── post.py
│   │   └── like.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── topic.py
│   │   └── post.py
│   └── routers/
│       ├── auth.py
│       ├── users.py
│       ├── categories.py
│       ├── topics.py
│       └── posts.py
├── alembic/
├── tests/
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

## Модели базы данных

### User

Пользователь форума.

Основные поля:

- `id`
- `username`
- `email`
- `hashed_password`
- `is_active`
- `created_at`

### Category

Категория форума.

Основные поля:

- `id`
- `name`
- `description`
- `created_at`

### Topic

Тема форума.

Основные поля:

- `id`
- `title`
- `author_id`
- `category_id`
- `created_at`
- `updated_at`

### Post

Сообщение внутри темы.

Основные поля:

- `id`
- `content`
- `author_id`
- `topic_id`
- `created_at`
- `updated_at`

### Like

Лайк сообщения.

Основные поля:

- `id`
- `user_id`
- `post_id`
- `created_at`

Один пользователь может поставить конкретному сообщению только один лайк.

## Установка проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/USERNAME/mini-forum.git
cd mini-forum
```

Замените `USERNAME` на имя владельца репозитория.

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

Активировать на Linux:

```bash
source .venv/bin/activate
```

Активировать на Windows:

```bash
.venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать файл `.env`

Скопировать пример:

```bash
cp .env.example .env
```

Пример содержимого:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/mini_forum
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Не загружайте настоящий файл `.env` на GitHub.

Секретный ключ можно создать командой:

```bash
openssl rand -hex 32
```

### 5. Создать базу данных PostgreSQL

```sql
CREATE DATABASE mini_forum;
```

### 6. Применить миграции

```bash
alembic upgrade head
```

### 7. Запустить приложение

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу:

```text
http://127.0.0.1:8000
```

## Документация API

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

OpenAPI-схема:

```text
http://127.0.0.1:8000/openapi.json
```

## Основные endpoints

### Авторизация

| Метод | Адрес | Описание |
|---|---|---|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/login` | Получение JWT |

### Пользователь

| Метод | Адрес | Описание |
|---|---|---|
| GET | `/users/me` | Получить свой профиль |
| PATCH | `/users/me` | Изменить свой профиль |

### Категории

| Метод | Адрес | Описание |
|---|---|---|
| GET | `/categories` | Получить категории |
| GET | `/categories/{category_id}` | Получить одну категорию |

### Темы

| Метод | Адрес | Описание |
|---|---|---|
| GET | `/topics` | Получить темы |
| GET | `/topics/{topic_id}` | Получить тему |
| POST | `/topics` | Создать тему |
| PATCH | `/topics/{topic_id}` | Изменить свою тему |
| DELETE | `/topics/{topic_id}` | Удалить свою тему |

### Сообщения

| Метод | Адрес | Описание |
|---|---|---|
| GET | `/topics/{topic_id}/posts` | Получить сообщения темы |
| POST | `/topics/{topic_id}/posts` | Написать сообщение |
| PATCH | `/posts/{post_id}` | Изменить своё сообщение |
| DELETE | `/posts/{post_id}` | Удалить своё сообщение |

### Лайки

| Метод | Адрес | Описание |
|---|---|---|
| POST | `/posts/{post_id}/likes` | Поставить лайк |
| DELETE | `/posts/{post_id}/likes` | Убрать лайк |

## Фильтрация и поиск

Получить темы определённой категории:

```http
GET /topics?category_id=1
```

Найти тему по названию:

```http
GET /topics?search=jwt
```

Использовать пагинацию:

```http
GET /topics?limit=10&offset=0
```

Параметры можно объединять:

```http
GET /topics?category_id=2&search=fastapi&limit=10&offset=0
```

## Запуск тестов

```bash
pytest
```

Подробный вывод:

```bash
pytest -v
```

## Правила доступа

- Смотреть категории, темы и сообщения могут все.
- Создавать контент могут только авторизованные пользователи.
- Пользователь может изменять и удалять только собственные темы.
- Пользователь может изменять и удалять только собственные сообщения.
- ID автора определяется по JWT.
- `author_id` нельзя передавать в теле запроса.
- Неактивный пользователь не может создавать контент.

## HTTP-коды

| Код | Значение |
|---:|---|
| `200` | Запрос успешно выполнен |
| `201` | Объект создан |
| `204` | Объект удалён |
| `401` | Пользователь не авторизован |
| `403` | Недостаточно прав |
| `404` | Объект не найден |
| `409` | Email или username уже занят |
| `422` | Ошибка валидации |

## Работа с Git

Для каждой задачи создаётся отдельная ветка:

```text
feature/auth-register
feature/auth-login
feature/topics-crud
feature/posts-crud
feature/likes
test/auth
fix/topic-permissions
```

Пример создания ветки:

```bash
git switch main
git pull
git switch -c feature/auth-login
```

После выполнения задачи:

```bash
git add .
git commit -m "feat: add JWT login"
git push -u origin feature/auth-login
```

После этого создаётся Pull Request. Второй разработчик проверяет код перед объединением с `main`.

## Авторы

- Разработчик 1: имя или ссылка на GitHub
- Разработчик 2: имя или ссылка на GitHub

## Статус проекта

Учебный проект находится в разработке.