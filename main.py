import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSlot, QVariant
from backend.apps import get_installed_apps_all
from backend.database import get_installed_apps_from_db, save_apps_to_db, remove_apps_from_db

class AppManager(QObject):
    @pyqtSlot(list)
    def saveAppsToDatabase(self, apps):
        save_apps_to_db(apps)
        self.updateInstalledAppsDiff()

    @pyqtSlot(list)
    def removeAppsFromDatabase(self, apps):
        remove_apps_from_db(apps)
        self.updateInstalledAppsDiff()

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

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    installed_apps_all = get_installed_apps_all()
    installed_apps_db = get_installed_apps_from_db()

    installed_apps_all_set = {app['name'] for app in installed_apps_all}
    installed_apps_db_set = {app['name'] for app in installed_apps_db}

    installed_apps_diff_set = installed_apps_all_set - installed_apps_db_set
    installed_apps_diff = sorted([{'name': name} for name in installed_apps_diff_set], key=lambda x: x['name'])

    print("Installed apps (diff):", installed_apps_diff)

    engine = QQmlApplicationEngine()

    context = engine.rootContext()
    context.setContextProperty("installedAppsDiff", installed_apps_diff)
    context.setContextProperty("installedAppsDB", installed_apps_db)
    context.setContextProperty("selectedAppsToAdd", [])
    context.setContextProperty("selectedAppsToRemove", [])

    app_manager = AppManager()
    context.setContextProperty("appManager", app_manager)

    engine.load("UI/base.qml")  # Указываем главный файл QML

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
