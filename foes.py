from dataclasses import dataclass
import random
from artifacts import Artifact
from weapon import Weapon, weapons
from armor import Armor

@dataclass
class FoeCharacteristics():
    HP: int = 100
    maxHP: int = 100
    dexterity: int = 10


class Foe:
    def __init__(
            self, 
            name: str,
            characteristics: FoeCharacteristics, 
            ):
        self.HP = characteristics.HP
        self.name = name
        self.maxHP = characteristics.maxHP
        self.dexterity = characteristics.dexterity
        self.isAlive = True 
    @property
    def attackDamage(self) -> int:
        return self.weapon.weaponDmg
    def takePhysicalDamage(self, damage):
        self.HP = self.HP - damage
        print(f'{self.name} получает {damage} единиц урона.')
        if self.HP <= 0:
            print(f'{self.name} погиб')
            self.isAlive = False
        else:
            print(f'У {self.name} остается {self.HP} хп')

        
    def takeMageDamage(self, mageDamage):
        self.HP -= mageDamage
        print(f'{self.name} получает {mageDamage} единиц магического урона.')
        if self.HP <= 0:
            print(f'{self.name} погиб')
            self.isAlive = False
        else:
            print(f'У {self.name} остается {self.HP} хп')

    def attack(self, targets):
        target = random.choice(targets)
        print(f'{self.name} ударил {getattr(target, "name")}, ' + 
              f'используя {self.weapon.weaponName}, с силой {self.attackDamage}')
        target.takePhysicalDamage(self.attackDamage)
        
    def makeMove(self, targets):
        if not len(targets):
            print(f'Похоже все уже мертвы')
            return 0
        if self.isAlive:
            self.attack(targets)
        else: print(f'{self.name} не может продолжать бой')
        
    def getName(self):
        return self.name

wolfChar = FoeCharacteristics(**{"HP": 80, "dexterity": 60})
ghostChar = FoeCharacteristics(**{"HP": 200, "dexterity": 40})
sphinxChar = FoeCharacteristics(**{"HP": 400, "dexterity": 10})
zombieChar = FoeCharacteristics(**{"HP":250, "dexterity": 1})


class Wolf(Foe):
    def __init__(self, name, characteristics: FoeCharacteristics=wolfChar):
        super().__init__(name, characteristics)
        self.className = "Wolf"
        self.type = "Dire wolf" 
        self.weapon = weapons.foe["jaw"]

class Ghost(Foe):
    def __init__(self, name, characteristics: FoeCharacteristics=ghostChar):
        super().__init__(name, characteristics)
        self.className = "Ghost"
        self.type = "Frightful banshee"
        self.weapon = weapons.foe["claws"]


class Sphinx(Foe):
    def __init__(self, name, characteristics: FoeCharacteristics=sphinxChar):
        super().__init__(name, characteristics)
        self.className = "Sphinx"
        self.type = "Wise sphinx"
        self.weapon = weapons.foe["fist"]

class Zombie(Foe):
    def __init__(self, name, characteristics: FoeCharacteristics=zombieChar):
        super().__init__(name, characteristics)
        self.className = "Zombie"
        self.type = "Dread zombie"
        self.weapon = weapons.foe["filthy mouth"]



