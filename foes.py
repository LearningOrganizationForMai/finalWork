from dataclasses import dataclass
import random
from typing import List, Any
from weapon import Weapon, weapons


@dataclass
class FoeCharacteristics:
    """
    Базовые характеристики врага (противника)   
    Атрибуты:
        HP (int): Текущее здоровье
        maxHP (int): Максимальное здоровье
        dexterity (int): Ловкость 
    """
    HP: int = 100
    maxHP: int = 100
    dexterity: int = 10


class Foe:
    """
    Базовый класс для всех врагов 
    Предполагается, что у каждого врага будет атрибут 'weapon'
    """
    def __init__(
        self,
        name: str,
        characteristics: FoeCharacteristics,
    ) -> None:
        self.name: str = name
        self.HP: int = characteristics.HP
        self.maxHP: int = characteristics.maxHP
        self.dexterity: int = characteristics.dexterity
        self.isAlive: bool = True

    @property
    def attackDamage(self) -> int:
        # Возвращает урон оружия врага
        return self.weapon.weaponDmg

    def takePhysicalDamage(self, damage: int) -> None:
        # Наносит физический урон
        self.HP -= damage
        print(f'{self.name} получает {damage} единиц урона.')
        if self.HP <= 0:
            print(f'{self.name} погиб')
            self.isAlive = False
        else:
            print(f'У {self.name} остается {self.HP} хп')

    def takeMageDamage(self, mageDamage: int) -> None:
        # Наносит магический урон
        self.HP -= mageDamage
        print(f'{self.name} получает {mageDamage} единиц магического урона.')
        if self.HP <= 0:
            print(f'{self.name} погиб')
            self.isAlive = False
        else:
            print(f'У {self.name} остается {self.HP} хп')

    def attack(self, targets: List[Any]) -> None:
        # Атакует случайную цель из списка 
        target = random.choice(targets)
        print(f'{self.name} ударил {getattr(target, "name")}, '
              f'используя {self.weapon.weaponName}, с силой {self.attackDamage}')
        target.takePhysicalDamage(self.attackDamage)

    def makeMove(self, targets: List[Any]) -> int:
        """
        Выполняет ход врага: атакует, если жив и есть цели
        Возвращает 0 для согласованности с боевой системой
        """
        if not len(targets):
            print(f'Похоже все уже мертвы')
            return 0
        if self.isAlive:
            self.attack(targets)
        else:
            print(f'{self.name} не может продолжать бой')
        return 0

    def getName(self) -> str:
        # Возвращает имя врага
        return self.name


# Предопределённые характеристики для каждого типа врага

wolfChar: FoeCharacteristics = FoeCharacteristics(**{"HP": 80, "dexterity": 60})
ghostChar: FoeCharacteristics = FoeCharacteristics(**{"HP": 200, "dexterity": 40})
sphinxChar: FoeCharacteristics = FoeCharacteristics(**{"HP": 400, "dexterity": 10})
zombieChar: FoeCharacteristics = FoeCharacteristics(**{"HP": 250, "dexterity": 1})


class Wolf(Foe):
    # Волк — быстрый, но слабый
    def __init__(self, name: str, characteristics: FoeCharacteristics = wolfChar) -> None:
        super().__init__(name, characteristics)
        self.className: str = "Wolf"
        self.type: str = "Dire wolf"
        self.weapon: Weapon = weapons.foe["jaw"]


class Ghost(Foe):
    # Привидение — средняя живучесть и скорость
    def __init__(self, name: str, characteristics: FoeCharacteristics = ghostChar) -> None:
        super().__init__(name, characteristics)
        self.className: str = "Ghost"
        self.type: str = "Frightful banshee"
        self.weapon: Weapon = weapons.foe["claws"]


class Sphinx(Foe):
    # Сфинкс — медленный, но очень живучий
    def __init__(self, name: str, characteristics: FoeCharacteristics = sphinxChar) -> None:
        super().__init__(name, characteristics)
        self.className: str = "Sphinx"
        self.type: str = "Wise sphinx"
        self.weapon: Weapon = weapons.foe["fist"]


class Zombie(Foe):
    # Зомби — крайне медленный, но с высоким HP
    def __init__(self, name: str, characteristics: FoeCharacteristics = zombieChar) -> None:
        super().__init__(name, characteristics)
        self.className: str = "Zombie"
        self.type: str = "Dread zombie"
        self.weapon: Weapon = weapons.foe["filthy mouth"]