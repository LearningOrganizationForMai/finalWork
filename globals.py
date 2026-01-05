from classes import Archer, Healer, Mage, Warrior


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