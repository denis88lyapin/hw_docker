Приложение hw_drf. 

Инструкция по запуску.
Шаг 1. Клонировать репозиторий.
Шаг 2. Установить зависимости.
Шаг 3. Установить postgresql
Шаг 4. Применить миграции.
Шаг 5. Заполнить базу:
    python manage.py loaddata school.json
Шаг 6. Создать пользователей: 
    python manage.py fill_usr
Шаг 7. Создать платежи:
    python manage.py fill_pay
Шаг 8. Запустить сервер

