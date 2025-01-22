from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
import sys

from managers import DatabaseManager, OpenedWindowsManager, TrackedAppsManager
from models.opened_windows_model import OpenedWindowsModel
from models.tracked_apps_model import TrackedAppsModel
from models.stats_model import StatsModel  # Импортируем модель статистики


if __name__ == "__main__":
    app = QApplication(sys.argv)

    statsModel = StatsModel()


    # Модель для открытых окон
    opened_windows_model = OpenedWindowsModel()

    tracked_apps_model = TrackedAppsModel()
    # Менеджеры
    opened_windows_manager = OpenedWindowsManager()
    tracked_apps_manager = TrackedAppsManager()
    database_manager = DatabaseManager()

    # Связываем модель с менеджером
    opened_windows_manager.openedWindowsModel = opened_windows_model

    # Устанавливаем связь между менеджерами
    opened_windows_manager.setTrackedAppsManager(tracked_apps_manager)
    tracked_apps_manager.databaseManager = database_manager  # Связываем с DatabaseManager

    tracked_apps_manager.updateTrackedApps()

    # Инициализация QML
    engine = QQmlApplicationEngine()
    context = engine.rootContext()

    # Передаем модели и менеджеры в QML
    context.setContextProperty("openedWindowsModel", opened_windows_model)
    context.setContextProperty("openedWindowsManager", opened_windows_manager)
    context.setContextProperty("trackedAppsManager", tracked_apps_manager)
    context.setContextProperty("trackedAppsModel", tracked_apps_manager.trackedAppsModel)  # Передаем модель
    context.setContextProperty("databaseManager", database_manager)
    context.setContextProperty("statsModel", statsModel)

    # Загружаем QML
    engine.load("UI/base.qml")

    # Проверяем, загрузился ли QML
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())