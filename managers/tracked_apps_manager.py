# managers/tracked_apps_manager.py
from PyQt5.QtCore import QObject, pyqtSlot
from backend.database import get_apps_from_tracked_apps_db
from models.tracked_apps_model import TrackedAppsModel


class TrackedAppsManager(QObject):
    def __init__(self):
        super().__init__()
        self._trackedAppsModel = TrackedAppsModel()  # Модель для отслеживаемых приложений

    @property
    def trackedAppsModel(self):
        """
        Возвращает модель отслеживаемых приложений.
        """
        return self._trackedAppsModel

    @pyqtSlot()
    def updateTrackedApps(self):
        """
        Обновляет список отслеживаемых приложений из базы данных.
        """
        trackedApps = get_apps_from_tracked_apps_db()  # Получаем данные из базы данных
        self._trackedAppsModel.updateData(trackedApps)  # Обновляем модель
        print("Список отслеживаемых приложений обновлен:", trackedApps)