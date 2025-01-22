# managers/database_manager.py
from PyQt5.QtCore import QObject, pyqtSlot
from backend.database import save_tracked_apps_db, remove_tracked_apps_db  # Новый метод


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


