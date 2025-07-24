# task-management-system

Веб-приложение на FastAPI с асинхронным доступом к PostgreSQL для управления задачами пользователей. Каждый пользователь может создавать, обновлять, получать и удалять свои задачи.



## Технологии

- Python 3.12  
- FastAPI  
- PostgreSQL  
- SQLAlchemy (асинхронный режим)  
- Alembic (миграции)  
- Docker & docker-compose  
- Pytest (тесты)  


## Установка и запуск

1. Клонирование репозитория

```bash
git clone https://github.com/MrRuzal/task-management-system.git
cd task-management-system
```

2. Создайте файл .env на основе .env.example и настройте параметры подключения к БД

3. Запуск через Docker Compose

```bash
docker-compose up --build
```


## Миграции

Alembic автоматически применяет миграции при старте контейнера через команду:

```sh
alembic upgrade head
```

Эта команда уже добавлена в `entrypoint.sh`, поэтому **никакие действия вручную выполнять не требуется**.


### Документация API

Доступна в браузере по адресу:
Swagger UI: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`



## Тестирование

Для запуска тестов используется `pytest`. Перед запуском убедитесь, что зависимости установлены и проект не требует подключения к реальной БД (используется мок).

```bash
pytest
```

Автор: [MrRuzal](https://github.com/MrRuzal)