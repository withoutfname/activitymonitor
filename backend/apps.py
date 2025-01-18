import winapps

def get_installed_apps_all():
    apps = []
    for app in winapps.list_installed():
        apps.append({
            'name': app.name,
        })
    return apps

