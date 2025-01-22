# managers/opened_windows_manager.py
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty
from backend.opened_windows import get_opened_windows


class OpenedWindowsManager(QObject):
    def __init__(self):
        super().__init__()
        self._runningAppsToAdd = []  # Массив для хранения отмеченных приложений
        self._trackedAppsManager = None  # Ссылка на TrackedAppsManager

    @pyqtProperty(list)
    def runningAppsToAdd(self):
        return self._runningAppsToAdd

    @runningAppsToAdd.setter
    def runningAppsToAdd(self, value):
        if self._runningAppsToAdd != value:
            self._runningAppsToAdd = value

    def setTrackedAppsManager(self, trackedAppsManager):
        """
        Устанавливает ссылку на TrackedAppsManager.
        """
        self._trackedAppsManager = trackedAppsManager

    @pyqtSlot()
    def updateOpenedWindows(self):
        """Обновление списка открытых окон."""
        if not self._trackedAppsManager:
            print("TrackedAppsManager не установлен!")
            return

        # Получаем список открытых окон
        windows = get_opened_windows()

        # Получаем список отслеживаемых приложений из модели
        tracked_apps = self._trackedAppsManager.trackedAppsModel.getTrackedApps()

        # Извлекаем exePath из отслеживаемых приложений
        tracked_exe_paths = [app["exePath"] for app in tracked_apps]

        # Фильтруем окна, исключая те, которые уже есть в отслеживаемых приложениях
        filtered_windows = [
            window for window in windows
            if window["exePath"] not in tracked_exe_paths
        ]

        # Обновляем модель
        self.openedWindowsModel.updateData(filtered_windows)
        self.filterRunningAppsToAdd()  # Фильтруем массив runningAppsToAdd

    def filterRunningAppsToAdd(self):
        """Фильтрует массив runningAppsToAdd, оставляя только запущенные приложения."""
        self._runningAppsToAdd = [
            app for app in self._runningAppsToAdd
            if self.openedWindowsModel.isAppRunning(app["processName"])
        ]
        print("Массив runningAppsToAdd обновлен после фильтрации:", self._runningAppsToAdd)