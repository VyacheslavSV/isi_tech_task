# Simple Chat Application

## Опис

Цей проєкт є простим чат-додатком, створеним за допомогою Django і Django REST Framework. Він підтримує базові функції
обміну повідомленнями між користувачами.

## Вимоги

- Python 3.8+
- Django 4.x
- Django REST Framework
- Simple JWT
- SQLite

## Як запустити проєкт

1. Клонуйте репозиторій:
    ```bash
    git clone <repository-url>
    cd project-directory
    ```

2. Створіть та активуйте віртуальне середовище:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux / MacOS
    venv\Scripts\activate  # Для Windows
    ```

3. Встановіть залежності:
    ```bash
    pip install -r requirements.txt
    ```

4. Застосуйте міграції:
    ```bash
    python manage.py migrate
    ```

5. Завантажте тестові дані (за потреби):
    ```bash
    python manage.py loaddata app_chat/fixtures/test_data.json
    ```

6. Запустіть сервер:
    ```bash
    python manage.py runserver
    ```
7. Для завантаження дампу бази данних:
    - за потреби очистити
    ```bash
    python manage.py flush
    ```
    - завантаженння дампу
    ```bash
    python manage.py loaddata db_dump.json
    ```
    - старт серверу
    ```bash
    python manage.py runserver
    ```

## Тестування

Для запуску тестів:

```bash
python manage.py tests/test_api.py
python manage.py tests/test_models.py