import json
import os


def read_file(file) -> dict:
    if not os.path.exists(file):
        with open(file, 'w', encoding='utf-8') as file1:
            json.dump({}, file1)
        return {}
    with open(file, 'r', encoding='utf-8') as file1:
        return json.load(file1)

