Приложение hw_drf. 

Инструкция по запуску.
Шаг 1. Клонировать репозиторий.
Шаг 2. Запустить docker:
    sudo docker compose up --build

Работа с приложением:
Шаг 1. Создать суперпользователя:
    python manage.py csu
    # email = "admin@mail.ru"
    # password = "admin"
Шаг 2. Создать пользователей и группу moderators: 
    python manage.py fill_usr
    user
    # email = "test@test.ru" - в группе moderators
    # password = "test"
    user1
    # email = "test1@test.ru"
    # password = "test1"
    user2
    # email = "test2@test.ru"
    # password = "test2"
Шаг 3. Заполнить базу:
    python manage.py loaddata school.json
Шаг 4. Создать платежи:
    python manage.py fill_pay
Шаг 5. Запустить сервер
Шаг 6. Запустить задачи celery
    celery -A config worker -l INFO
    celery -A config beat -l info -S django



