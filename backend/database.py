import psycopg2
import os
from functools import wraps


def get_db_connection():
    """
    Возвращает соединение с базой данных.
    """
    return psycopg2.connect(
        dbname="activitydb",  # Название вашей базы данных
        user="postgres",  # Пользователь PostgreSQL
        password="pass",  # Ваш пароль
        host="localhost",  # Хост (локально)
        port="5432"  # Порт по умолчанию
    )


def create_tables():
    """
    Создает таблицы в базе данных, если они не существуют.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tracked_apps (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        exe_path VARCHAR(255),
                        process_name VARCHAR(255)
                    );
                """)


                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS activity_sessions (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        process_name VARCHAR(255),
                        exe_path VARCHAR(255),
                        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        end_time TIMESTAMP,
                        is_tracking BOOLEAN DEFAULT TRUE
                    );
                """)


    except Exception as e:
        print("Ошибка при создании таблиц:", e)


def ensure_tables_exist(func):
    """
    Декоратор, который гарантирует, что таблицы существуют перед выполнением функции.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        create_tables()  # Создаем таблицы, если их нет
        return func(*args, **kwargs)  # Выполняем основную функцию
    return wrapper


@ensure_tables_exist
def save_tracked_apps_db(apps):
    """
    Сохраняет приложения с путями (exe_path) и названиями процессов (process_name) в таблицу tracked_apps.
    Принимает массив объектов, где каждый объект содержит:
    - title (название приложения)
    - processName (название процесса)
    - exePath (путь к исполняемому файлу)
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Вставка данных в таблицу tracked_apps
                for app in apps:
                    cursor.execute("""
                        INSERT INTO tracked_apps (name, exe_path, process_name)
                        VALUES (%s, %s, %s)
                    """, (app["title"], app["exePath"], app["processName"]))

                # Сохранение изменений
                conn.commit()

    except Exception as e:
        print(f"Ошибка при добавлении данных в таблицу: {e}")


@ensure_tables_exist
def remove_tracked_apps_db(apps):
    """
    Удаляет приложения из таблицы tracked_apps по имени, пути и названию процесса.
    Принимает массив объектов, где каждый объект содержит:
    - title (название приложения)
    - processName (название процесса)
    - exePath (путь к исполняемому файлу)
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Удаление данных из таблицы tracked_apps
                for app in apps:
                    cursor.execute("""
                        DELETE FROM tracked_apps
                        WHERE name = %s AND exe_path = %s AND process_name = %s;
                    """, (app["title"], app["exePath"], app["processName"]))

                # Сохранение изменений
                conn.commit()

    except Exception as e:
        print(f"Ошибка при удалении данных из таблицы: {e}")


@ensure_tables_exist
def get_apps_from_tracked_apps_db():
    """
    Возвращает список приложений из таблицы tracked_apps.
    Каждый элемент списка — это словарь с ключами:
    - name (название приложения)
    - exePath (путь к исполняемому файлу)
    - processName (название процесса)
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Выполнение запроса
                cursor.execute("SELECT name, exe_path, process_name FROM tracked_apps")

                # Получение данных
                rows = cursor.fetchall()

                # Преобразование данных в список словарей
                apps = [
                    {
                        "name": row[0],
                        "exePath": row[1],
                        "processName": row[2]
                    }
                    for row in rows
                ]
                return apps
    except Exception as e:
        print(f"Ошибка при получении данных из базы данных: {e}")
        return []