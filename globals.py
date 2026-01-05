from classes import Archer, Healer, Mage, Warrior

# Создаем глобальные переменные, которые будут нужны, чтобы можно было использовать их из любых функций
USER = None
SAVE_FILE = 'save.json'
USERS_FILE = 'users.json'
HASH_ITERATIONS = 100_000
STAGE = 1
STAGE_LIMIT = 3
CLASS_MAP={
    "Warrior": Warrior,
    "Archer": Archer,
    "Mage": Mage,
    "Healer": Healer,
}