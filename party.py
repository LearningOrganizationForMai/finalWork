from typing import List, Dict, Any
from character import Characteristics
from classes import Archer, Healer, Mage, Warrior
from weapon import weapons
from armor import armors
import globals


# Предопределённый отряд по умолчанию для новой игры
aragorn = Warrior(
    'Aragorn',
    weapons.warrior.swords["exscalibur"],
    armors.warrior["fullplate"]
)

legolas = Archer(
    'Legolas',
    weapons.archer.bows["galadhrim"],
    armors.archer["leather"]
)

abaddon = Mage(
    'Abaddon',
    weapons.mage.staffs["mysticStaff"],
    armors.mage["robe"]
)

chen = Healer(
    'Chen',
    weapons.mage.staffs["staffOfWizardry"],  
    armors.healer["chainmail"]
)

defaultParty: List = [aragorn, legolas, abaddon, chen]


def createPartyFromSave(party: List[Dict[str, Any]], classMap: Dict[str, Any] = globals.CLASS_MAP) -> List[Any]:
    """
    Воссоздаёт отряд из данных сохранения
    Для каждого персонажа в сохранении:
      Определяет класс
      Находит соответствующее оружие и доспех в глобальных реестрах
      Создаёт экземпляр класса с восстановленными характеристиками и артефактами
    Аргументы:
        party (List[dict]): Список словарей с данными персонажей из сохранения
        classMap (dict): Отображение имени класса → конструктор класса из globals
    Возвращает:
        List[Character]: Список восстановленных объектов персонажей
    """
    new_party: List[Any] = []
    for char in party:
        className: str = char["className"].lower()
        weaponClass: str = char["weapon"]["weaponClass"]
        weaponName: str = char["weapon"]["weaponName"]
        
        # Динамически получаем оружие
        weapon = getattr(
            getattr(weapons, className),
            weaponClass
        )[weaponName]
        
        # Получаем доспех 
        armor = getattr(armors, className)[char["armor"]]
        
        # Создаём персонажа нужного класса
        loadedCharacter = classMap[char["className"]](
            name=char["name"],
            weapon=weapon,
            armor=armor,
            characteristics=mapCharacteristics(char)
        )
        
        # Загружаем артефакты 
        loadedCharacter.loadArtifacts(char["artifacts"])
        new_party.append(loadedCharacter)
    
    return new_party


def mapCharacteristics(data: Dict[str, Any]) -> Characteristics:
    """
    Преобразует словарь характеристик из сохранения в объект Characteristics
    Аргументы:
        data (dict): Словарь с ключами "HP", "MP", "strength", "dexterity", "intelligence"
    Возвращает:
        Characteristics: Объект характеристик персонажа
    """
    return Characteristics(
        HP=data["HP"],
        MP=data["MP"],
        strength=data["strength"],
        dexterity=data["dexterity"],
        intelligence=data["intelligence"]
    )


def getArtifacts(party: List[Any]) -> List[List[str]]:
    """
    Извлекает списки артефактов у всех персонажей в отряде
    Аргументы:
        party (List[Character]): Список объектов персонажей
    Возвращает:
        List[List[str]]: Список списков названий артефактов (по одному подсписку на персонажа)
    """
    artifacts: List[List[str]] = []
    for char in party:
        artifacts.append(char.showArtifacts())
    return artifacts