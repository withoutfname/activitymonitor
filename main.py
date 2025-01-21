from PyQt5.QtCore import QObject, pyqtSlot, QAbstractListModel, Qt, QModelIndex, QVariant, pyqtSignal, pyqtProperty
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
import sys

from backend.database import get_names_from_installed_apps_db
from backend.installed_apps import get_installed_apps_all
from backend.opened_windows import get_opened_windows


class OpenedWindowsModel(QAbstractListModel):
    def __init__(self, windows=None):
        super().__init__()
        self.windows = windows or []
        self.filtered_windows = self.windows  # Изначально отображаем все окна
        self._filter_text = ""  # Текущий текст фильтра

    def rowCount(self, parent=QModelIndex()):
        return len(self.filtered_windows)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        window = self.filtered_windows[index.row()]

        if role == Qt.DisplayRole:
            return window["title"]
        elif role == Qt.UserRole:
            return window["processName"]
        elif role == Qt.UserRole + 1:
            return window["exePath"]
        return QVariant()

    def roleNames(self):
        return {
            Qt.DisplayRole: b"title",
            Qt.UserRole: b"processName",
            Qt.UserRole + 1: b"exePath",
        }

    def updateData(self, new_windows):
        self.beginResetModel()
        self.windows = new_windows
        self._applyFilter()  # Применяем фильтр после обновления данных
        self.endResetModel()

    @pyqtSlot(str)
    def filter(self, text):
        """Фильтрация списка окон по тексту."""
        self._filter_text = text
        self._applyFilter()

    def _applyFilter(self):
        """Применяет текущий фильтр к списку окон."""
        self.beginResetModel()
        if self._filter_text:
            self.filtered_windows = [window for window in self.windows if self._filter_text.lower() in window["title"].lower()]
        else:
            self.filtered_windows = self.windows  # Если фильтр пуст, показываем все окна
        self.endResetModel()


class InstalledAppsModel(QAbstractListModel):
    def __init__(self, apps=None):
        super().__init__()
        self.apps = apps or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.apps)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        app = self.apps[index.row()]

        if role == Qt.DisplayRole or role == Qt.UserRole:
            return app["name"]
        elif role == Qt.UserRole + 1:
            return app.get("exe_path", "")

        return QVariant()

    def roleNames(self):
        return {
            Qt.DisplayRole: b"name",
            Qt.UserRole: b"name",
            Qt.UserRole + 1: b"exePath",
        }

    def updateData(self, new_apps):
        self.beginResetModel()
        self.apps = new_apps
        self.endResetModel()


class AppManager(QObject):
    def __init__(self):
        super().__init__()
        self._is_tracking = False  # Состояние отслеживания

    isTrackingChanged = pyqtSignal()

    @pyqtProperty(bool, notify=isTrackingChanged)
    def isTracking(self):
        return self._is_tracking

    @isTracking.setter
    def isTracking(self, value):
        if self._is_tracking != value:
            self._is_tracking = value
            self.isTrackingChanged.emit()

    @pyqtSlot()
    def startTracking(self):
        """Запуск отслеживания открытых окон."""
        self.isTracking = True

    @pyqtSlot()
    def stopTracking(self):
        """Остановка отслеживания."""
        self.isTracking = False

    @pyqtSlot()
    def updateOpenedWindows(self):
        """Обновление списка открытых окон."""
        windows = get_opened_windows()
        self.openedWindowsModel.updateData(windows)

    @pyqtSlot(list)
    def saveAppsToDatabase(self, apps):
        print("Сохраненные приложения:", apps)


def not_tracked_apps(installed_apps_all, short_db_apps):
    """
    Фильтрует приложения, которые есть в installed_apps_all,
    но отсутствуют в short_installed_apps.
    """
    short_db_names = {app["name"] for app in short_db_apps}
    new_apps = [
        app for app in installed_apps_all if app["name"] not in short_db_names
    ]
    return new_apps


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Получение данных
    installed_apps_all = get_installed_apps_all()  # Все установленные приложения
    short_db_apps = get_names_from_installed_apps_db()  # Приложения из short_installed_apps

    # Фильтрация новых приложений
    not_tracked_apps = not_tracked_apps(installed_apps_all, short_db_apps)

    # Создание моделей
    all_apps_model = InstalledAppsModel(installed_apps_all)  # Модель для всех приложений
    short_db_apps_model = InstalledAppsModel(short_db_apps)  # Модель для приложений из БД
    not_tracked_apps_model = InstalledAppsModel(not_tracked_apps)  # Модель для новых приложений
    opened_windows_model = OpenedWindowsModel()  # Модель для открытых окон

    # Инициализация QML
    engine = QQmlApplicationEngine()

    # Установка контекстов
    context = engine.rootContext()
    context.setContextProperty("allAppsModel", all_apps_model)  # Все установленные приложения
    context.setContextProperty("shortDbAppsModel", short_db_apps_model)  # Приложения из БД
    context.setContextProperty("notTrackedAppsModel", not_tracked_apps_model)  # Только новые приложения
    context.setContextProperty("openedWindowsModel", opened_windows_model)

    app_manager = AppManager()
    app_manager.openedWindowsModel = opened_windows_model
    context.setContextProperty("appManager", app_manager)

    # Загрузка QML
    engine.load("UI/base.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())