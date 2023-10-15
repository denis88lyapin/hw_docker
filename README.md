Приложение hw_drf. 

Инструкция по запуску.
Шаг 1. Клонировать репозиторий.
Шаг 2. Установить зависимости.
Шаг 3. Установить postgresql
Шаг 4. Применить миграции.
Шаг 5. Создать суперпользователя:
    python manage.py csu
    # email = "admin@mail.ru"
    # password = "admin"
Шаг 6. Создать пользователей и группу moderators: 
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
Шаг 7. Заполнить базу:
    python manage.py loaddata school.json
Шаг 8. Создать платежи:
    python manage.py fill_pay
Шаг 9. Запустить сервер
Шаг 10. Запустить задачи celery
    celery -A config worker -l INFO
    celery -A config beat -l info -S django



