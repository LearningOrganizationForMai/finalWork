from dataclasses import dataclass
import random
from typing import List, Dict, Any, Optional
from artifacts import artifacts
from weapon import Weapon
from armor import Armor


@dataclass
class Characteristics:
    """
    Характеристики персонажа: здоровье, мана, силы и тд
    По умолчанию заданы базовые значения для обычного персонажа
    """
    HP: int = 200
    maxHP: int = 200
    MP: int = 0
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 0


class Character:
    """
    Базовый класс для всех персонажей в игре
    Атрибуты:
        name (str): Имя персонажа
        className (str): Класс персонажа 
        HP, maxHP, MP, strength, dexterity, intelligence — боевые характеристики
        weapon (Weapon): Текущее оружие
        armor (Armor): Текущий доспех
        artifacts (List[Artifact]): Список полученных артефактов
        isAlive (bool): Флаг жив/мёртв
    """
    def __init__(
        self,
        name: str,
        weapon: Weapon,
        armor: Armor,
        characteristics: Characteristics,
    ) -> None:
        self.name: str = name
        self.className: str = "undefind"
        self.HP: int = characteristics.HP
        self.maxHP: int = characteristics.maxHP
        self.MP: int = characteristics.MP
        self.strength: int = characteristics.strength
        self.dexterity: int = characteristics.dexterity
        self.intelligence: int = characteristics.intelligence
        self.weapon: Weapon = weapon
        self.armor: Armor = armor
        self.artifacts: List[Any] = []
        self.isAlive: bool = True

    @property
    def attackDamage(self) -> int:
        # Возвращает урон от оружия без модификаторов силы (базовый урон оружия)
        return self.weapon.weaponDmg

    def takePhysicalDamage(self, damage: int) -> None:
        """
        Наносит физический урон с учётом защиты доспеха
        Урон уменьшается на значение брони, но не ниже нуля
        """
        # Расчёт финального урона после брони
        finishDamage: int = damage - self.armor.defense
        if finishDamage < 0:
            print("Броня заблокировала весь урон")
            finishDamage = 0
        self.HP -= finishDamage

        print(f'{self.name} получает {damage} единиц урона. '
              f'{self.armor.armorName} броня заблокировала {self.armor.defense} единиц урона. '
              f'{self.name} получает {finishDamage} единиц урона')

        if self.HP <= 0:
            print(f'{self.name} погиб')
            self.isAlive = False
        else:
            print(f'У {self.name} остается {self.HP} хп')

    def takeMageDamage(self, mageDamage: int) -> None:
        # Наносит магический урон, игнорирующий броню
        self.HP -= mageDamage
        print(f'{self.name} получает {mageDamage} единиц магического урона.')
        if self.HP <= 0:
            print(f'{self.name} погиб')
            self.isAlive = False
        else:
            print(f'У {self.name} остается {self.HP} хп')

    def takeHeal(self, heal: int) -> None:
        # Восстанавливает здоровье, но не выше maxHP
        if self.HP + heal > self.maxHP:
            self.HP = self.maxHP
            print(f'{self.name} полностью излечивается. Теперь у него {self.HP} хп')
        else:
            self.HP += heal
            print(f'{self.name} получает лечение на {heal} единиц ХП. Теперь его ХП {self.HP}')

    def attack(self, target: Any) -> None:
        # Выполняет базовую атаку по цели
        print(f'{self.name} ударил {getattr(target, "name")}, '
              f'используя {self.weapon.weaponName}, с силой {self.attackDamage}')
        target.takePhysicalDamage(self.attackDamage)

    def makeMove(self, targets: List[Any]) -> int:
        """
        Выполняет стандартный ход: атакует случайную цель из списка живых врагов
        Возвращает 0, если нет целей или персонаж мёртв
        """
        if not len(targets):
            print(f'{self.name} хотел продолжить бой, но похоже все уже мертвы')
            return 0
        if self.isAlive:
            target = random.choice(targets)
            self.attack(target)
        else:
            print(f'{self.name} не может продолжать бой')
        return 0  

    def showArtifacts(self) -> List[str]:
        # Возвращает список названий артефактов, имеющихся у персонажа
        return [art.artifactName for art in self.artifacts]

    def getArtifact(self, art: Any) -> None:
        # Добавляет артефакт в инвентарь персонажа
        self.artifacts.append(art)
        print(f'{self.name} получает {getattr(art, "artifactName")}')

    def loadArtifacts(self, arts: List[str]) -> None:
        """
        Загружает артефакты по их названиям из глобального реестра 'artifacts'
        Использует имя класса персонажа (в нижнем регистре) для определения категории
        """
        for art in arts:
            # Динамически получаем словарь артефактов для класса персонажа
            self.artifacts.append(getattr(artifacts, self.className.lower())[art])

    def getSaveData(self) -> Dict[str, Any]:
        # Возвращает данные персонажа в виде словаря для сохранения 
        return {
            "className": self.className,
            "name": self.name,
            "HP": self.HP,
            "MP": self.MP,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "intelligence": self.intelligence,
            "weapon": {
                "weaponName": self.weapon.weaponName,
                "weaponClass": self.weapon.weaponClass
            },
            "armor": self.armor.armorName,
            "artifacts": [art.artifactName for art in self.artifacts]
        }
