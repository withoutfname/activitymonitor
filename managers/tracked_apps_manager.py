# managers/tracked_apps_manager.py

from PyQt5.QtCore import QObject, pyqtSlot, QTimer, QDateTime, Qt
from backend.database import get_apps_from_tracked_apps_db, start_activity, end_activity
from models.tracked_apps_model import TrackedAppsModel
import psutil  # Используем psutil для работы с процессами


class TrackedAppsManager(QObject):
    def __init__(self):
        super().__init__()
        self._trackedAppsModel = TrackedAppsModel()  # Модель для отслеживаемых приложений
        self.runningProcesses = {}  # Словарь для хранения запущенных процессов

        # Таймер для периодической проверки процессов
        self.timer = QTimer()
        self.timer.timeout.connect(self.checkRunningProcesses)
        self.timer.start(5000)  # Проверка каждые 5 секунд
        self.checkRunningProcesses()

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

    def checkRunningProcesses(self):
        """
        Проверяет запущенные процессы и сравнивает их с отслеживаемыми приложениями.
        """
        trackedApps = self._trackedAppsModel.getTrackedApps()  # Получаем список отслеживаемых приложений
        runningProcesses = self.getRunningProcesses()  # Получаем список запущенных процессов

        # Проверяем, какие из отслеживаемых приложений запущены
        for app in trackedApps:
            exePath = app["exePath"]
            appName = app["name"]
            processName = app["processName"]

            # Проверяем, запущен ли процесс по пути (exePath) ИЛИ по имени (processName)
            if self.isProcessRunning(exePath, processName, runningProcesses):
                if exePath not in self.runningProcesses:
                    # Приложение запущено
                    self.runningProcesses[exePath] = QDateTime.currentDateTime()  # Сохраняем время начала
                    start_activity(appName, processName, exePath)  # Запускаем активность
                    print(f"Приложение {appName} запущено.")
            else:
                if exePath in self.runningProcesses:
                    # Приложение завершено
                    del self.runningProcesses[exePath]
                    end_activity(appName, processName, exePath)  # Завершаем активность
                    print(f"Приложение {appName} завершено.")

    def getRunningProcesses(self):
        """
        Возвращает список запущенных процессов с использованием psutil.
        """
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    processInfo = proc.info
                    processes.append({
                        "pid": processInfo['pid'],
                        "name": processInfo['name'],
                        "exe": processInfo['exe']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Пропускаем процессы, к которым нет доступа
                    continue
        except Exception as e:
            print(f"Ошибка при получении списка процессов: {e}")

        #print("Запущенные процессы:", processes)  # Отладочный вывод
        return processes

    def isProcessRunning(self, exePath, processName, runningProcesses):
        """
        Проверяет, запущен ли процесс по пути (exePath) или по имени (processName).
        """
        for proc in runningProcesses:
            # Сравниваем по полному пути к исполняемому файлу
            if exePath and proc["exe"] and exePath.lower() == proc["exe"].lower():
                return True
            # Сравниваем по имени процесса
            if processName and proc["name"] and processName.lower() == proc["name"].lower():
                return True
        return False

    @pyqtSlot(result=int)
    def getRunningTrackedAppsCount(self):
        """
        Возвращает количество запущенных отслеживаемых приложений.
        """
        return len(self.runningProcesses)

    @pyqtSlot(result="QVariantList")
    def getIncompleteActivities(self):
        """
        Возвращает список незавершенных активностей с текущей длительностью.
        """
        incomplete_activities = []
        current_time = QDateTime.currentDateTime()

        for exePath, startTime in self.runningProcesses.items():
            # Находим приложение в списке отслеживаемых
            trackedApps = self._trackedAppsModel.getTrackedApps()
            for app in trackedApps:
                if app["exePath"] == exePath:
                    incomplete_activities.append({
                        "name": app["name"],
                        "exePath": exePath,
                        "start_time": startTime.toString(Qt.ISODate),  # Преобразуем время в строку
                        "current_duration": startTime.secsTo(current_time)  # Текущая длительность в секундах
                    })
                    break

        return incomplete_activities