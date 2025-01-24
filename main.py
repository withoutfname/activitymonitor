import os

import psycopg2
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
import sys

from backend.database import get_db_connection
from managers import openedWindowsManager, trackedAppsManager, appMonitorManager, statsManager, \
    statCleaningManager
from models import openedWindowsModel, trackedAppsModel, statCleaningModel

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        connection = get_db_connection()
        print("Успешное подключение к базе данных!")
        connection.close()
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")

    # Модели
    opened_windows_model = openedWindowsModel()
    tracked_apps_model = trackedAppsModel()
    stat_cleaning_model = statCleaningModel()

    # Менеджеры
    opened_windows_manager = openedWindowsManager()
    tracked_apps_manager = trackedAppsManager()
    stat_cleaning_manager = statCleaningManager()
    stats_manager = statsManager()

    # Связываем модель с менеджером
    opened_windows_manager.openedWindowsModel = opened_windows_model
    stat_cleaning_manager._model = stat_cleaning_model


    # Устанавливаем связь между менеджерами
    opened_windows_manager.setTrackedAppsManager(tracked_apps_manager)
    app_monitor_manager = appMonitorManager(tracked_apps_manager)

    # Вызываем функции менеджеров
    tracked_apps_manager.updateTrackedApps()
    app_monitor_manager.checkRunningProcesses()

    # Инициализация QML
    engine = QQmlApplicationEngine()
    context = engine.rootContext()

    # Передаем менеджеры в QML
    context.setContextProperty("openedWindowsManager", opened_windows_manager)
    context.setContextProperty("trackedAppsManager", tracked_apps_manager)
    context.setContextProperty("appMonitorManager", app_monitor_manager)
    context.setContextProperty("statCleaningManager", stat_cleaning_manager)
    context.setContextProperty("statsManager", stats_manager)

    # Передаем модели в QML
    context.setContextProperty("openedWindowsModel", opened_windows_model)
    context.setContextProperty("trackedAppsModel", tracked_apps_manager.trackedAppsModel)
    engine.rootContext().setContextProperty("statCleaningModel", stat_cleaning_model)

    # Загружаем QML
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_file_path = os.path.join(current_dir, 'UI', 'base.qml')

    engine.load(qml_file_path)  # Загружаем QML-файл

    # Проверяем, загрузился ли QML
    if not engine.rootObjects():
        sys.exit(-1)

    def on_app_exit():
        app_monitor_manager.cleanupOnExit()

    app.aboutToQuit.connect(on_app_exit)

    sys.exit(app.exec())



