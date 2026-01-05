import json
import os
from typing import Dict, Any, Optional
import globals


def load_save(filename: str = globals.SAVE_FILE) -> Dict[str, Any]:
    """
    Загружает данные сохранения из JSON-файла
    Если файл не существует — создаёт пустой файл с пустым словарём
    Аргументы:
        filename (str): Путь к файлу сохранения
    Возвращает:
        dict: Содержимое файла сохранения (или пустой словарь)
    """
    if not os.path.exists(filename):
        # Создаём пустой файл сохранения, если он отсутствует
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return {}
    
    # Загружаем существующие данные
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_save(data: Dict[str, Any], filename: str = globals.SAVE_FILE) -> None:
    """
    Сохраняет данные в JSON-файл
    Аргументы:
        data (dict): Данные для сохранения
        filename (str): Путь к файлу сохранения
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_save_data(
    party: list, 
    previousLocation: Optional[Any], 
    oldData: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Формирует обновлённые данные сохранения для текущего пользователя
    Объединяет старые данные (для других пользователей) с новыми данными текущего игрока
    Аргументы:
        party (list): Список объектов персонажей
        previousLocation (Optional[Any]): Объект последней посещённой локации
        oldData (dict): Существующие данные сохранения
    Возвращает:
        dict: Обновлённый словарь данных для записи в файл
    """
    user_key: str = str(globals.USER)
    new_user_data: Dict[str, Any] = {
        "party": [person.getSaveData() for person in party],
        "stage": globals.STAGE,
        "previousLocation": previousLocation.title if previousLocation else None
    }
    # Объединяем старые данные с новыми
    return {
        **oldData,              # сохраняем данные других пользователей
        user_key: new_user_data  # обновляем или создаём запись текущего
    }