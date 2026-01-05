from dataclasses import dataclass, field
from typing import Literal, Dict, Any


# Типы оружия для каждого класса — используются для строгой типизации
WarriorWeaponType = Literal['swords', 'clubs']
ArcherWeaponType = Literal['bows', 'daggers']
MageWeaponType = Literal['staffs', 'scepter']
HealerWeaponType = Literal['staffs', 'scepter']


class Weapon:
    """
    Представляет оружие — предмет, дающий урон и принадлежащий к определённому типу
    Атрибуты:
        weaponName (str): Название оружия
        weaponDmg (int): Базовый урон
        weaponClass (str): Тип оружия
    """
    def __init__(self, weaponName: str, weaponDmg: int, weaponClass: str = "unknown") -> None:
        self.weaponName = weaponName
        self.weaponDmg = weaponDmg
        self.weaponClass = weaponClass


@dataclass
class WarriorWeapon:
    # Контейнер для оружия воина, разделённого по подтипам
    swords: Dict[str, Weapon] = field(default_factory=dict)
    clubs: Dict[str, Weapon] = field(default_factory=dict)


@dataclass
class ArcherWeapon:
    # Контейнер для оружия лучника
    bows: Dict[str, Weapon] = field(default_factory=dict)
    daggers: Dict[str, Weapon] = field(default_factory=dict)


@dataclass
class MageWeapon:
    # Контейнер для оружия мага
    staffs: Dict[str, Weapon] = field(default_factory=dict)
    scepter: Dict[str, Weapon] = field(default_factory=dict)


@dataclass
class HealerWeapon:
    # Контейнер для оружия целителя 
    staffs: Dict[str, Weapon] = field(default_factory=dict)
    scepter: Dict[str, Weapon] = field(default_factory=dict)


class Weapons:
    """
    Глобальный реестр всего оружия в игре, разбитого по ролям и типам
    Атрибуты:
        warrior (WarriorWeapon): Оружие воина
        archer (ArcherWeapon): Оружие лучника
        mage (MageWeapon): Оружие мага
        healer (HealerWeapon): Оружие целителя
        boss (Dict[str, Weapon]): Оружие боссов
        foe (Dict[str, Weapon]): Оружие обычных врагов
    """
    def __init__(self) -> None:
        self.warrior: WarriorWeapon = WarriorWeapon()
        self.archer: ArcherWeapon = ArcherWeapon()
        self.mage: MageWeapon = MageWeapon()
        self.healer: HealerWeapon = HealerWeapon()
        self.boss: Dict[str, Weapon] = {}
        self.foe: Dict[str, Weapon] = {}

    def addWarriorWeapon(self, weapon: Weapon, weaponType: WarriorWeaponType) -> None:
        # Добавляет оружие в соответствующую категорию воина
        getattr(self.warrior, weaponType)[weapon.weaponName] = weapon

    def addArcherWeapon(self, weapon: Weapon, weaponType: ArcherWeaponType) -> None:
        # Добавляет оружие в категорию лучника
        getattr(self.archer, weaponType)[weapon.weaponName] = weapon

    def addMageWeapon(self, weapon: Weapon, weaponType: MageWeaponType) -> None:
        # Добавляет оружие в категорию мага
        getattr(self.mage, weaponType)[weapon.weaponName] = weapon

    def addHealerWeapon(self, weapon: Weapon, weaponType: HealerWeaponType) -> None:
        # Добавляет оружие в категорию целителя
        getattr(self.healer, weaponType)[weapon.weaponName] = weapon

    def addBossWeapon(self, weapon: Weapon) -> None:
        # Добавляет оружие в коллекцию боссов
        self.boss[weapon.weaponName] = weapon

    def addFoeWeapon(self, weapon: Weapon) -> None:
        # Добавляет оружие в коллекцию обычных врагов
        self.foe[weapon.weaponName] = weapon



swords = {
    "exscalibur": Weapon("exscalibur", 10, "swords"), 
    "longsword": Weapon("longsword", 5, "swords"),
    "ashbringer": Weapon("ashbringer", 7, "swords") 
}

bows = {
    "shortBow": Weapon("shortBow", 5, "bows"),
    "longBow": Weapon("longBow", 7, "bows"),
    "galadhrim": Weapon("galadhrim", 10, "bows") 
}

staffs = {
    "mysticStaff": Weapon("mysticStaff", 10, "staffs"),
    "staffOfWizardry": Weapon("staffOfWizardry", 5, "staffs"),
    "staffOfPerplex": Weapon("staffOfPerplex", 7, "staffs")
}

bossWeapons = {
    "cleaver": Weapon("cleaver", 10),
    "hugeClub": Weapon("hugeClub", 20)
}

foeWeapons = {
    "claws": Weapon("claws", 30),
    "fist": Weapon("fist", 50),
    "jaw": Weapon("jaw", 25),
    "filthy mouth": Weapon("filthy mouth", 30)
}


# Создание глобального реестра оружия и регистрация всех предметов
weapons = Weapons()

# Регистрация оружия для воина
for i in swords.keys():
    weapons.addWarriorWeapon(swords[i], "swords")

# Регистрация оружия для лучника
for i in bows.keys():
    weapons.addArcherWeapon(bows[i], "bows")

# Регистрация оружия для мага
for i in staffs.keys():
    weapons.addMageWeapon(staffs[i], "staffs")

# Регистрация оружия для целителя, посохи как у мага
for i in staffs.keys():
    weapons.addHealerWeapon(staffs[i], "staffs")

# Регистрация оружия боссов
for weapon in bossWeapons.values():
    weapons.addBossWeapon(weapon)

# Регистрация оружия обычных врагов
for weapon in foeWeapons.values():
    weapons.addFoeWeapon(weapon)