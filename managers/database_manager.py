from PyQt5.QtCore import QObject, pyqtSlot
from backend.database import (
    save_tracked_apps_db,
    remove_tracked_apps_db,
    start_activity,
    end_activity,
    cleanup_incomplete_activities,
    get_app_stats,
    get_app_stats_last_2_weeks,
    get_app_stats_last_month,
    get_app_stats_last_year,
    add_or_update_alias,  # Новая функция для добавления/обновления псевдонима
    get_alias,  # Новая функция для получения псевдонима
    get_apps_from_tracked_apps_db, get_app_stats_all_time,
    get_incomplete_activities,  # Новая функция для получения приложений с псевдонимами
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

    @pyqtSlot(result="QVariantList")
    def getAppStatsLast2Weeks(self):
        """
        Возвращает статистику по приложениям за последние 2 недели.
        """
        return get_app_stats_last_2_weeks()

    @pyqtSlot(result="QVariantList")
    def getAppStatsLastMonth(self):
        """
        Возвращает статистику по приложениям за последний месяц.
        """
        return get_app_stats_last_month()

    @pyqtSlot(result="QVariantList")
    def getAppStatsLastYear(self):
        """
        Возвращает статистику по приложениям за последний год.
        """
        return get_app_stats_last_year()

    @pyqtSlot(str, str, str, str)
    def addOrUpdateAlias(self, name, process_name, exe_path, alias):
        """
        Добавляет или обновляет псевдоним для приложения.
        """
        add_or_update_alias(name, process_name, exe_path, alias)

    @pyqtSlot(str, str, str, result=str)
    def getAlias(self, name, process_name, exe_path):
        """
        Возвращает псевдоним для приложения по его name, process_name и exe_path.
        Если псевдоним не найден, возвращает пустую строку.
        """
        alias = get_alias(name, process_name, exe_path)
        return alias if alias else ""

    @pyqtSlot(result="QVariantList")
    def getAppsWithAliases(self):
        """
        Возвращает список приложений с псевдонимами.
        Каждый элемент списка — это словарь с ключами:
        - name (название приложения)
        - exePath (путь к исполняемому файлу)
        - processName (название процесса)
        - alias (псевдоним, если есть)
        """
        return get_apps_from_tracked_apps_db()

    @pyqtSlot(result="QVariantList")
    def getAppStatsAllTime(self):
        """
        Возвращает статистику по приложениям за всё время.
        """
        return get_app_stats_all_time()

    @pyqtSlot(result="QVariantList")
    def getIncompleteActivities(self):
        """
        Возвращает список незавершенных активностей.
        """
        return get_incomplete_activities()