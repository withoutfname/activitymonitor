from PyQt5.QtCore import QAbstractListModel, Qt, QModelIndex, pyqtProperty, pyqtSignal


class StatsModel(QAbstractListModel):
    # Сигнал для уведомления об изменении данных
    statsChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stats = []  # Массив для хранения статистики

    # Свойство count для QML
    @pyqtProperty(int, notify=statsChanged)
    def count(self):
        """
        Возвращает количество элементов в модели.
        """
        return len(self._stats)

    def rowCount(self, parent=QModelIndex()):
        """
        Возвращает количество элементов в модели.
        """
        return len(self._stats)

    def data(self, index, role=Qt.DisplayRole):
        """
        Возвращает данные для указанного индекса и роли.
        """
        if not index.isValid() or index.row() >= len(self._stats):
            return None

        stat = self._stats[index.row()]

        if role == Qt.DisplayRole:
            return stat["name"]  # Возвращаем имя приложения для отображения
        elif role == Qt.UserRole + 1:
            return stat["exePath"]  # Возвращаем путь к исполняемому файлу
        elif role == Qt.UserRole + 2:
            return stat["totalDuration"]  # Возвращаем общее время работы
        return None

    def roleNames(self):
        """
        Возвращает роли, которые поддерживает модель.
        """
        roles = {
            Qt.DisplayRole: b"name",  # Роль для отображения имени
            Qt.UserRole + 1: b"exePath",  # Роль для пути к исполняемому файлу
            Qt.UserRole + 2: b"totalDuration"  # Роль для общего времени работы
        }
        return roles

    def updateData(self, stats):
        """
        Обновляет данные модели.
        """
        self.beginResetModel()
        self._stats = stats
        self.endResetModel()
        self.statsChanged.emit()  # Уведомляем об изменении данных