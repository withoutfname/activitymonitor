# hooks/hook-psycopg2.py
from PyInstaller.utils.hooks import collect_data_files

# Указываем PyInstaller, что нужно включить данные для psycopg2
datas = collect_data_files('psycopg2')