import json
import os
import globals


def load_save(filename=globals.SAVE_FILE):
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return {}
    
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_save(data, filename=globals.SAVE_FILE):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_save_data(party, previousLocation, oldData: dict) -> dict:
    user_key = str(globals.USER)
    new_user_data = {
        "party": [person.getSaveData() for person in party],
        "stage": globals.STAGE,
        "previousLocation": previousLocation.title if previousLocation else None
    }
    return {
        **oldData,              # старые данные
        user_key: new_user_data # перезапись или создание ключа
    }

