import winreg

def get_installed_apps_all():
    """Получение списка установленных приложений из реестра и их пути к исполняемым файлам"""
    apps = []
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for reg_path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                exe_path = winreg.QueryValueEx(subkey, "InstallLocation")[0] if "InstallLocation" in [winreg.EnumValue(subkey, j)[0] for j in range(winreg.QueryInfoKey(subkey)[1])] else None
                                exe_path = exe_path or winreg.QueryValueEx(subkey, "DisplayIcon")[0]


                                apps.append({
                                    "name": app_name,
                                    "exe_path": exe_path,

                                })
                            except FileNotFoundError:
                                continue
                            except OSError:
                                continue
                    except FileNotFoundError:
                        continue
                    except OSError:
                        continue
        except FileNotFoundError:
            continue

    return apps
