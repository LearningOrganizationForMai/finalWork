class Armor:
    """
    Класс, представляющий доспех
    Атрибуты:
        armorName (str): Название доспеха
        defense (int): Значение защиты, которое даёт доспех
    """
    def __init__(self, armorName: str, defense: int) -> None:
        self.armorName = armorName
        self.defense = defense


class Armors:
    """
    Контейнер для хранения доспехов, разделённых по типам персонажей и боссов
    Атрибуты:
        warrior (Dict[str, Armor]): Доспехи для воина
        archer (Dict[str, Armor]): Доспехи для лучника
        mage (Dict[str, Armor]): Доспехи для мага
        healer (Dict[str, Armor]): Доспехи для целителя
        boss (Dict[str, Armor]): Доспехи для босса
    """
    def __init__(self) -> None:
        self.warrior: dict[str, Armor] = {}
        self.archer: dict[str, Armor] = {}
        self.mage: dict[str, Armor] = {}
        self.healer: dict[str, Armor] = {}
        self.boss: dict[str, Armor] = {}

    def addWarriorArmor(self, armor: Armor) -> None:
        # Добавляет доспех в коллекцию доспехов воина
        self.warrior[armor.armorName] = armor

    def addArcherArmor(self, armor: Armor) -> None:
        # Добавляет доспех в коллекцию доспехов лучника
        self.archer[armor.armorName] = armor

    def addMageArmor(self, armor: Armor) -> None:
        # Добавляет доспех в коллекцию доспехов мага
        self.mage[armor.armorName] = armor

    def addHealerArmor(self, armor: Armor) -> None:
        # Добавляет доспех в коллекцию доспехов целителя
        self.healer[armor.armorName] = armor

    def addBossArmor(self, armor: Armor) -> None:
        # Добавляет доспех в коллекцию доспехов босса
        self.boss[armor.armorName] = armor


# Словари с предопределёнными доспехами для каждой роли.
warriorArmor = {
    "fullplate": Armor("fullplate", 15)  # Тяжёлый доспех для воина
}

archerArmor = {
    "leather": Armor("leather", 7)       # Лёгкая кожаная броня для лучника
}

mageArmor = {
    "robe": Armor("robe", 2)            # Магическая мантия с минимальной защитой
}

healerArmor = {
    "chainmail": Armor("chainmail", 9)  # Кольчуга для целителя — баланс между защитой и мобильностью
}

bossArmor = {
    "bossArmor": Armor("bossArmor", 10) # Уникальный доспех босса
}


# Создание экземпляра контейнера доспехов.
armors = Armors()

# Проходим по значениям каждого словаря и добавляем доспехи через соответствующие методы.

for armor in warriorArmor.values():
    armors.addWarriorArmor(armor)

for armor in archerArmor.values():
    armors.addArcherArmor(armor)

for armor in mageArmor.values():
    armors.addMageArmor(armor)

for armor in healerArmor.values():
    armors.addHealerArmor(armor)

for armor in bossArmor.values():
    armors.addBossArmor(armor)