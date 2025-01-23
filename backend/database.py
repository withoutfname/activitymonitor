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

@ensure_tables_exist
def start_activity(app_name, process_name, exe_path):
    """
    Запускает новую активность для приложения.
    Заполняет start_time и устанавливает is_tracking в TRUE.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO activity_sessions (name, process_name, exe_path, start_time, is_tracking)
                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP, TRUE)
                """, (app_name, process_name, exe_path))

                # Сохранение изменений
                conn.commit()
                print(f"Активность для {app_name} начата.")

    except Exception as e:
        print(f"Ошибка при старте активности: {e}")

@ensure_tables_exist
def end_activity(app_name, process_name, exe_path):
    """
    Завершает активность для приложения.
    Заполняет end_time и устанавливает is_tracking в FALSE.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE activity_sessions
                    SET end_time = CURRENT_TIMESTAMP, is_tracking = FALSE
                    WHERE name = %s AND process_name = %s AND exe_path = %s AND is_tracking = TRUE
                """, (app_name, process_name, exe_path))

                # Сохранение изменений
                conn.commit()
                print(f"Активность для {app_name} завершена.")

    except Exception as e:
        print(f"Ошибка при завершении активности: {e}")

@ensure_tables_exist
def cleanup_incomplete_activities():
    """
    Завершает все активности, которые не были завершены (is_tracking = TRUE).
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE activity_sessions
                    SET end_time = CURRENT_TIMESTAMP, is_tracking = FALSE
                    WHERE is_tracking = TRUE
                """)

                # Сохранение изменений
                conn.commit()
                print("Незавершенные активности очищены.")

    except Exception as e:
        print(f"Ошибка при очистке незавершенных активностей: {e}")


@ensure_tables_exist
def get_app_stats():
    """
    Возвращает статистику по приложениям из таблицы activity_sessions.
    Вычисляет длительность как разницу между end_time и start_time.
    """
    stats = []
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        name, 
                        exe_path, 
                        SUM(EXTRACT(EPOCH FROM (end_time - start_time))) as total_duration
                    FROM activity_sessions
                    WHERE end_time IS NOT NULL  -- Исключаем незавершенные сессии
                    GROUP BY name, exe_path
                """)
                rows = cursor.fetchall()

                # Преобразуем данные в список словарей
                for row in rows:
                    stats.append({
                        "name": row[0],
                        "exePath": row[1],
                        "totalDuration": int(row[2])  # Преобразуем в целое число (секунды)
                    })
    except Exception as e:
        print(f"Ошибка при получении статистики: {e}")

    return stats

@ensure_tables_exist
def get_incomplete_activities():
    """
    Возвращает список незавершенных активностей (где end_time IS NULL).
    Каждый элемент списка — это словарь с ключами:
    - name (название приложения)
    - start_time (время начала отслеживания)
    """
    incomplete_activities = []
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT name, start_time
                    FROM activity_sessions
                    WHERE end_time IS NULL
                """)
                rows = cursor.fetchall()

                # Преобразуем данные в список словарей
                for row in rows:
                    incomplete_activities.append({
                        "name": row[0],
                        "start_time": row[1].isoformat()  # Преобразуем время в строку
                    })
    except Exception as e:
        print(f"Ошибка при получении незавершенных активностей: {e}")

    return incomplete_activities

# backend/database.py

@ensure_tables_exist
def delete_incomplete_activities():
    """
    Удаляет все незавершенные активности (где end_time IS NULL).
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM activity_sessions
                    WHERE end_time IS NULL
                """)

                # Сохранение изменений
                conn.commit()
                print("Незавершенные активности удалены.")

    except Exception as e:
        print(f"Ошибка при удалении незавершенных активностей: {e}")


@ensure_tables_exist
def get_app_stats_last_2_weeks():
    """
    Возвращает статистику по приложениям за последние 2 недели.
    """
    stats = []
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        name,
                        exe_path,
                        SUM(EXTRACT(EPOCH FROM (end_time - start_time))) as total_duration
                    FROM activity_sessions
                    WHERE end_time IS NOT NULL
                      AND start_time >= NOW() - INTERVAL '2 weeks'
                    GROUP BY name, exe_path
                """)
                rows = cursor.fetchall()

                for row in rows:
                    stats.append({
                        "name": row[0],
                        "exePath": row[1],
                        "totalDuration": int(row[2])
                    })
    except Exception as e:
        print(f"Ошибка при получении статистики за последние 2 недели: {e}")

    return stats

@ensure_tables_exist
def get_app_stats_last_month():
    """
    Возвращает статистику по приложениям за последний месяц.
    """
    stats = []
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        name,
                        exe_path,
                        SUM(EXTRACT(EPOCH FROM (end_time - start_time))) as total_duration
                    FROM activity_sessions
                    WHERE end_time IS NOT NULL
                      AND start_time >= NOW() - INTERVAL '1 month'
                    GROUP BY name, exe_path
                """)
                rows = cursor.fetchall()

                for row in rows:
                    stats.append({
                        "name": row[0],
                        "exePath": row[1],
                        "totalDuration": int(row[2])
                    })
    except Exception as e:
        print(f"Ошибка при получении статистики за последний месяц: {e}")

    return stats

@ensure_tables_exist
def get_app_stats_last_year():
    """
    Возвращает статистику по приложениям за последний год.
    """
    stats = []
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        name,
                        exe_path,
                        SUM(EXTRACT(EPOCH FROM (end_time - start_time))) as total_duration
                    FROM activity_sessions
                    WHERE end_time IS NOT NULL
                      AND start_time >= NOW() - INTERVAL '1 year'
                    GROUP BY name, exe_path
                """)
                rows = cursor.fetchall()

                for row in rows:
                    stats.append({
                        "name": row[0],
                        "exePath": row[1],
                        "totalDuration": int(row[2])
                    })
    except Exception as e:
        print(f"Ошибка при получении статистики за последний год: {e}")

    return stats
