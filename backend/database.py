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
                print("Таблица tracked_apps создана успешно!")

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
                print("Таблица activity_sessions создана успешно!")

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
                print(f"{len(apps)} приложений успешно добавлены в таблицу tracked_apps!")
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
                print(f"{len(apps)} приложений успешно удалены из таблицы tracked_apps!")
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







'''


def save_apps_to_db(apps):
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            dbname="activitydb",
            user="postgres",
            password="pass",
            host="localhost",
            port="5432"
        )

        # Создание курсора
        cursor = conn.cursor()

        # Вставка данных в таблицу
        for app in apps:
            cursor.execute("INSERT INTO installed_apps (name) VALUES (%s)", (app,))


        # Сохранение изменений
        conn.commit()

        # Закрытие курсора и соединения
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")


def remove_apps_from_db(apps):
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            dbname="activitydb",
            user="postgres",
            password="pass",
            host="localhost",
            port="5432"
        )

        # Создание курсора
        cursor = conn.cursor()

        # Удаление данных из таблицы
        for app in apps:
            cursor.execute("DELETE FROM installed_apps WHERE name = %s", (app,))
            cursor.execute("""
                            UPDATE global_stats
                            SET end_time = CURRENT_TIMESTAMP, is_tracking = FALSE
                            WHERE name = %s AND is_tracking = TRUE
                        """, (app,))

        # Сохранение изменений
        conn.commit()

        # Закрытие курсора и соединения
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

def get_global_stats_from_db():
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            dbname="activitydb",
            user="postgres",
            password="pass",
            host="localhost",
            port="5432"
        )

        # Создание курсора
        cursor = conn.cursor()

        # Выполнение запроса
        cursor.execute("SELECT name, start_time, end_time, is_tracking FROM global_stats")

        # Получение данных
        rows = cursor.fetchall()

        # Закрытие курсора и соединения
        cursor.close()
        conn.close()

        # Преобразование данных в список словарей
        stats = [{'name': row[0], 'start_time': row[1], 'end_time': row[2], 'is_tracking': row[3]} for row in rows]
        return stats

    except Exception as e:
        print(f"Error: {e}")
        return []

def start_activity_session(app_name):
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            dbname="activitydb",
            user="postgres",
            password="pass",
            host="localhost",
            port="5432"
        )

        # Создание курсора
        cursor = conn.cursor()

        # Вставка данных в таблицу
        cursor.execute("INSERT INTO activity_sessions (app_name) VALUES (%s)", (app_name,))

        # Сохранение изменений
        conn.commit()

        # Закрытие курсора и соединения
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

def end_activity_session(app_name):
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            dbname="activitydb",
            user="postgres",
            password="pass",
            host="localhost",
            port="5432"
        )

        # Создание курсора
        cursor = conn.cursor()

        # Обновление данных в таблице
        cursor.execute("UPDATE activity_sessions SET end_time = CURRENT_TIMESTAMP WHERE app_name = %s AND end_time IS NULL", (app_name,))
        print(f'Postgres обновил {app_name}')

        # Проверка, что запрос обновил хотя бы одну запись
        if cursor.rowcount == 0:
            print(f"No matching record found for {app_name}")

        # Сохранение изменений
        conn.commit()

        # Закрытие курсора и соединения
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")
'''