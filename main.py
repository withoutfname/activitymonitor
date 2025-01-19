import sys
from PyQt5 import QtWidgets
import psutil
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSlot, QVariant, QTimer
from PyQt5.QtWidgets import QApplication
from backend.apps import get_installed_apps_all
from backend.database import get_installed_apps_from_db, save_apps_to_db, remove_apps_from_db, get_global_stats_from_db, start_activity_session, end_activity_session

class AppManager(QObject):
    @pyqtSlot(list)
    def saveAppsToDatabase(self, apps):
        save_apps_to_db(apps)
        self.updateInstalledAppsDiff()

    @pyqtSlot(list)
    def removeAppsFromDatabase(self, apps):
        remove_apps_from_db(apps)
        self.updateInstalledAppsDiff()

    @pyqtSlot()
    def updateInstalledAppsDiff(self):
        installed_apps_all = get_installed_apps_all()
        installed_apps_db = get_installed_apps_from_db()

        installed_apps_all_set = {app['name'] for app in installed_apps_all}
        installed_apps_db_set = {app['name'] for app in installed_apps_db}

        installed_apps_diff_set = installed_apps_all_set - installed_apps_db_set
        installed_apps_diff = sorted([{'name': name} for name in installed_apps_diff_set], key=lambda x: x['name'])

        context = engine.rootContext()
        context.setContextProperty("installedAppsDiff", installed_apps_diff)
        context.setContextProperty("installedAppsDB", installed_apps_db)
        context.setContextProperty("globalStats", get_global_stats_from_db())

    def checkInstalledApps(self):
        installed_apps_all = get_installed_apps_all()
        installed_apps_db = get_installed_apps_from_db()

        installed_apps_all_set = {app['name'] for app in installed_apps_all}
        installed_apps_db_set = {app['name'] for app in installed_apps_db}

        uninstalled_apps = installed_apps_db_set - installed_apps_all_set
        if uninstalled_apps:
            self.showUninstalledAppsDialog(list(uninstalled_apps))

    def showUninstalledAppsDialog(self, uninstalled_apps):
        # Показать диалоговое окно с предложением удалить неактуальные приложения
        dialog = QtWidgets.QMessageBox()
        dialog.setIcon(QtWidgets.QMessageBox.Warning)
        dialog.setWindowTitle("Неактуальные приложения")
        dialog.setText("Следующие приложения больше не установлены на вашем компьютере:")
        dialog.setInformativeText("\n".join(uninstalled_apps))
        dialog.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        dialog.setDefaultButton(QtWidgets.QMessageBox.Ok)

        ret = dialog.exec_()
        if ret == QtWidgets.QMessageBox.Ok:
            self.removeAppsFromDatabase(uninstalled_apps)
        else:
            sys.exit(0)

    def __init__(self):
        super().__init__()
        self.running_apps = {}

    def monitor_apps(self):
        installed_apps = get_installed_apps_from_db()
        installed_apps_set = {self.normalize_name(app['name']): app['name'] for app in installed_apps}

        for proc in psutil.process_iter(['name']):
            try:
                proc_name = self.normalize_name(proc.info['name'])
                if proc_name in installed_apps_set and proc_name not in self.running_apps:
                    original_name = installed_apps_set[proc_name]
                    print(f"Приложение {original_name} запущено.")
                    start_activity_session(original_name)
                    self.running_apps[proc_name] = original_name
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Проверка завершения процессов
        for proc_name in list(self.running_apps.keys()):
            if not any(self.normalize_name(proc.info['name']) == proc_name for proc in psutil.process_iter(['name'])):
                original_name = self.running_apps[proc_name]
                print(f"Приложение {original_name} завершено.")
                end_activity_session(original_name)
                del self.running_apps[proc_name]

        QTimer.singleShot(5000, self.monitor_apps)  # Проверяем каждые 5 секунд

    def normalize_name(self, name):
        # Удаляем расширения файлов и символы, которые могут мешать сравнению
        name = name.lower().replace('.exe', '').replace(' ', '').replace('-', '')
        return name

if __name__ == "__main__":
    app = QApplication(sys.argv)

    installed_apps_all = get_installed_apps_all()
    installed_apps_db = get_installed_apps_from_db()

    installed_apps_all_set = {app['name'] for app in installed_apps_all}
    installed_apps_db_set = {app['name'] for app in installed_apps_db}

    installed_apps_diff_set = installed_apps_all_set - installed_apps_db_set
    installed_apps_diff = sorted([{'name': name} for name in installed_apps_diff_set], key=lambda x: x['name'])
    print(installed_apps_db)

    engine = QQmlApplicationEngine()

    context = engine.rootContext()
    context.setContextProperty("installedAppsDiff", installed_apps_diff)
    context.setContextProperty("installedAppsDB", installed_apps_db)
    context.setContextProperty("selectedAppsToAdd", [])
    context.setContextProperty("selectedAppsToRemove", [])
    context.setContextProperty("globalStats", get_global_stats_from_db())

    app_manager = AppManager()
    context.setContextProperty("appManager", app_manager)

    engine.load("UI/base.qml")  # Указываем главный файл QML

    if not engine.rootObjects():
        sys.exit(-1)

    # Проверка установленных приложений при запуске
    app_manager.checkInstalledApps()

    # Запуск мониторинга приложений
    app_manager.monitor_apps()

    sys.exit(app.exec())
