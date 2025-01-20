import win32gui
import win32process
import psutil
from datetime import datetime

def get_opened_windows():
    """Получение списка всех видимых окон и связанных с ними процессов."""
    windows = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            title = win32gui.GetWindowText(hwnd)
            if title:  # Учитываем только окна с заголовками
                windows.append((hwnd, pid, title))

    win32gui.EnumWindows(callback, None)
    return windows

def main():
    open_windows = get_opened_windows()
    for hwnd, pid, title in open_windows:
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            exe_path = process.exe()  # Путь к исполняемому файлу
            create_time = datetime.fromtimestamp(process.create_time())  # Время запуска процесса
            parent_hwnd = win32gui.GetParent(hwnd)  # Родительское окно

            print(f"Process: {process_name}")
            print(f"Exe Path: {exe_path}")
            print(f"Start Time: {create_time.strftime('%Y-%m-%d %H:%M:%S')}")

        except psutil.NoSuchProcess:
            continue
        except psutil.AccessDenied:
            print(f"Access Denied for PID {pid}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
