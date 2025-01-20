import psycopg2

# Подключение к базе данных PostgreSQL
connection = psycopg2.connect(
    dbname="activitydb",  # Название вашей базы данных
    user="postgres",  # Пользователь PostgreSQL
    password="pass",  # Ваш пароль
    host="localhost",  # Хост (локально)
    port="5432"  # Порт по умолчанию
)

# Создание таблицы
try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS short_installed_apps (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,                                
                short_exe_path VARCHAR(255)                            
                );
            """)
            print("Таблица создана успешно!")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS full_installed_apps (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    full_exe_path VARCHAR(255),
                    short_exe_path VARCHAR(255),
                    process_name VARCHAR(255)
                );
            """)
            print("Таблица создана успешно!")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS global_stats (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    process_name VARCHAR(255),
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP,
                    is_tracking BOOLEAN DEFAULT TRUE
                );
            """)
            print("Таблица создана успешно!")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_sessions (
                    id SERIAL PRIMARY KEY,
                    app_name VARCHAR(255) NOT NULL,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP
                );
            """)
            print("Таблицы созданы успешно!")
except Exception as e:
    print("Ошибка при создании таблицы:", e)
finally:
    connection.close()



def save_apps_to_short_db(apps, paths):
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            dbname="activitydb",  # Название вашей базы данных
            user="postgres",  # Пользователь PostgreSQL
            password="pass",  # Ваш пароль
            host="localhost",  # Хост (локально)
            port="5432"  # Порт по умолчанию
        )

        # Создание курсора
        cursor = conn.cursor()

        # Вставка данных в таблицу short_installed_apps
        for app, path in zip(apps, paths):
            cursor.execute("""
                INSERT INTO short_installed_apps (name, short_exe_path) 
                VALUES (%s, %s)
                """, (app, path))

        # Сохранение изменений
        conn.commit()
        print(f"{len(apps)} приложений успешно добавлены в таблицу short_installed_apps!")

    except Exception as e:
        print(f"Ошибка при добавлении данных в таблицу: {e}")
    finally:
        # Закрытие курсора и соединения
        cursor.close()
        conn.close()





'''
def get_installed_apps_from_db():
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
        cursor.execute("SELECT name FROM installed_apps")

        # Получение данных
        rows = cursor.fetchall()

        # Закрытие курсора и соединения
        cursor.close()
        conn.close()

        # Преобразование данных в список словарей
        apps = [{'name': row[0]} for row in rows]
        return apps

    except Exception as e:
        print(f"Error: {e}")
        return []

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