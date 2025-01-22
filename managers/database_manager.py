# managers/database_manager.py
from PyQt5.QtCore import QObject, pyqtSlot
from backend.database import save_tracked_apps_db  # Новый метод


class DatabaseManager(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(list)
    def saveAppsToDatabase(self, apps):
        """
        Сохраняет приложения в базу данных.
        """
        save_tracked_apps_db(apps)
        print("Приложения сохранены в базу данных:", apps)

