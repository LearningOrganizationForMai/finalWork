import os
import hashlib
import binascii
import json
from typing import Dict, Any, Optional
from file_system import read_file
import globals


def hash_password(password: str) -> Dict[str, str]:
    """
    Генерирует хеш пароля с использованием случайной соли
    Аргументы:
        password (str): Исходный пароль в виде строки
    Возвращает:
        dict: Словарь с ключами 'salt' и 'hash', оба в виде hex-строк
    """
    # Генерация криптографически безопасной случайной соли 16 бит
    salt: bytes = os.urandom(16)
    
    # Вычисление хеша с заданным количеством итераций из глобальных настроек
    hash_bytes: bytes = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        globals.HASH_ITERATIONS
    )

    # Преобразование байтов в hex-строки для удобного хранения
    return {
        'salt': binascii.hexlify(salt).decode('utf-8'),
        'hash': binascii.hexlify(hash_bytes).decode('utf-8')
    }


def verify_password(password: str, stored: Dict[str, str]) -> bool:
    """
    Проверяет, соответствует ли введённый пароль сохранённому хешу
    Аргументы:
        password (str): Введённый пользователем пароль
        stored (dict): Словарь с 'salt' и 'hash' из хранилища
    Возвращает:
        bool: True, если пароль верен; иначе False
    """
    # Преобразуем hex-строку соли обратно в байты
    salt: bytes = binascii.unhexlify(stored['salt'])
    
    # Пересчитываем хеш на основе введённого пароля и сохранённой соли
    new_hash: bytes = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        globals.HASH_ITERATIONS
    )
    
    # Сравниваем полученный хеш с сохранённым (в виде hex-строк)
    return binascii.hexlify(new_hash).decode('utf-8') == stored['hash']


def save_info(users: Dict[str, Any], file: str) -> None:
    """
    Сохраняет словарь пользователей в JSON-файл с читаемым форматированием
    Аргументы:
        users (dict): Словарь пользователей
        file (str): Путь к файлу
    """
    with open(file, 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


def registration(login: str, password: str) -> None:
    """
    Регистрирует нового пользователя
    Если логин уже существует — выводит ошибку
    Иначе — создаёт нового пользователя с уникальным ID и сохраняет данные
    """
    users: Dict[str, Any] = read_file(globals.USERS_FILE)
    
    if login in users:
        print(f"Ошибка: пользователь '{login}' уже существует")
        return
    
    # Генерация нового уникального ID: максимум существующих + 1, или 1 при пустом файле
    new_id: int = max(
        (user['id'] for user in users.values()),
        default=0
    ) + 1

    # Добавление нового пользователя
    users[login] = {
        'id': new_id,
        'login': login,
        'password': hash_password(password)
    }
    
    # Установка текущего пользователя в глобальную переменную
    globals.USER = new_id
    
    # Сохранение обновлённого списка пользователей
    save_info(users, globals.USERS_FILE)
    print(f"Пользователь '{login}' успешно зарегистрирован")


def login(login: str, password: str) -> None:
    """
    Выполняет вход пользователя по логину и паролю
    Если логин не найден — ошибка
    Если пароль неверен — сообщение об ошибке
    Иначе — установка globals.USER и подтверждение входа
    """
    users: Dict[str, Any] = read_file(globals.USERS_FILE)
    
    if login not in users:
        print(f"Пользователя с логином {login} не существует")
        return
    
    if verify_password(password, users[login]["password"]):
        id: int = users[login]['id']
        globals.USER = id
        print(f"Вы вошли в аккаунт")
    else:
        print("Не верно введен пароль")