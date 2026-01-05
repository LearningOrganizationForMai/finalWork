from dataclasses import dataclass, field
from typing import Literal

WarriorWeaponType = Literal['swords', 'clubs']
ArcherWeaponType = Literal['bows', 'daggers']
MageWeaponType = Literal['staffs', 'scepter']
HealerWeaponType = Literal['staffs', 'scepter']

class Weapon():
    def __init__(self, weaponName, weaponDmg, weaponClass="unknown"):
        self.weaponName = weaponName
        self.weaponDmg = weaponDmg
        self.weaponClass = weaponClass


@dataclass
class WarriorWeapon:
    swords: dict[str, Weapon] = field(default_factory=dict)
    clubs: dict[str, Weapon] = field(default_factory=dict)

@dataclass
class ArcherWeapon:
    bows: dict[str, Weapon] = field(default_factory=dict)
    daggers: dict[str, Weapon] = field(default_factory=dict)

@dataclass
class MageWeapon:
    staffs: dict[str, Weapon] = field(default_factory=dict)
    scepter: dict[str, Weapon] = field(default_factory=dict)
    
@dataclass
class HealerWeapon:
    staffs: dict[str, Weapon] = field(default_factory=dict)
    scepter: dict[str, Weapon] = field(default_factory=dict)


class Weapons:
    def __init__(self):
        self.warrior: WarriorWeapon = WarriorWeapon()
        self.archer: ArcherWeapon = ArcherWeapon()
        self.mage: MageWeapon = MageWeapon()
        self.healer: HealerWeapon = HealerWeapon()
        self.boss: dict[str, Weapon] = {}
        self.foe: dict[str, Weapon] = {}

    def addWarriorWeapon(self, weapon: Weapon, weaponType: WarriorWeaponType):
        getattr(self.warrior, weaponType)[weapon.weaponName] = weapon
        
    def addArcherWeapon(self, weapon: Weapon, weaponType: ArcherWeaponType):
        getattr(self.archer, weaponType)[weapon.weaponName] = weapon

    def addMageWeapon(self, weapon: Weapon, weaponType: MageWeaponType):
        getattr(self.mage, weaponType)[weapon.weaponName] = weapon

    def addHealerWeapon(self, weapon: Weapon, weaponType: HealerWeaponType):
        getattr(self.healer, weaponType)[weapon.weaponName] = weapon

    def addBossWeapon(self, weapon: Weapon):
        self.boss[weapon.weaponName] = weapon

    def addFoeWeapon(self, weapon: Weapon):
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

weapons = Weapons()
for i in swords.keys():
    weapons.addWarriorWeapon(swords[i], "swords")

for i in bows.keys():
    weapons.addArcherWeapon(bows[i], "bows")

for i in staffs.keys():
    weapons.addMageWeapon(staffs[i], "staffs")
    
for i in staffs.keys():
    weapons.addHealerWeapon(staffs[i], "staffs")

for weapon in bossWeapons.values():
    weapons.addBossWeapon(weapon)

for weapon in foeWeapons.values():
    weapons.addFoeWeapon(weapon)
