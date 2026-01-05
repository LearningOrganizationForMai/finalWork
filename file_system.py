import json
import os
from typing import Dict


def read_file(file: str) -> Dict:
    """
    Читает JSON-файл и возвращает его содержимое в виде словаря
    Если файл не существует — создаёт пустой JSON-файл с пустым словарём
    и возвращает пустой словарь
    Аргументы:
        file (str): Путь к файлу
    Возвращает:
        dict: Содержимое файла (или пустой словарь, если файл не существовал)
    """
    if not os.path.exists(file):
        # Создаём новый файл, если он отсутствует
        with open(file, 'w', encoding='utf-8') as file1: 
            json.dump({}, file1)
        return {}
    
    # Читаем существующий файл
    with open(file, 'r', encoding='utf-8') as file1: 
        return json.load(file1)