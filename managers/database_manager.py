# managers/database_manager.py
from PyQt5.QtCore import QObject, pyqtSlot
from backend.database import (
    save_tracked_apps_db,
    remove_tracked_apps_db,
    start_activity,
    end_activity,
    cleanup_incomplete_activities, get_app_stats,
)


class DatabaseManager(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(list)
    def saveAppsToDatabase(self, apps):
        """
        Сохраняет приложения в базу данных.
        """
        save_tracked_apps_db(apps)

    @pyqtSlot(list)
    def removeAppsFromDatabase(self, apps):
        """
        Удаляет приложения из базы данных.
        Принимает список объектов, где каждый объект содержит:
        - title (название приложения)
        - exePath (путь к исполняемому файлу)
        - processName (название процесса)
        """
        remove_tracked_apps_db(apps)

    @pyqtSlot(str, str, str)
    def startActivity(self, app_name, process_name, exe_path):
        """
        Запускает новую активность для приложения.
        """
        start_activity(app_name, process_name, exe_path)

    @pyqtSlot(str, str, str)
    def endActivity(self, app_name, process_name, exe_path):
        """
        Завершает активность для приложения.
        """
        end_activity(app_name, process_name, exe_path)

    @pyqtSlot(str, str, str)
    def updateActivity(self, app_name, process_name, exe_path):
        """
        Обновляет активность для приложения, если оно завершило работу.
        """
        cleanup_incomplete_activities(app_name, process_name, exe_path)

    @pyqtSlot(result="QVariantList")
    def getAppStats(self):
        """
        Возвращает статистику по приложениям из таблицы activity_sessions.
        """
        return get_app_stats()