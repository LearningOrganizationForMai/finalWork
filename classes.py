import random
from typing import List, Dict, Any, Optional
from character import Character, Characteristics
from weapon import weapons, Weapon
from armor import armors, Armor
from spells import spells, MageSpell, HealSpell
from abilities import abilities


# Предопределённые характеристики для каждого класса
warriorChar: Characteristics = Characteristics(**{"HP": 200, "strength": 56, "dexterity": 40})
archerChar: Characteristics = Characteristics(**{"HP": 200, "dexterity": 50})
mageChar: Characteristics = Characteristics(**{"dexterity": 35, "MP": 140, "intelligence": 50})
healChar: Characteristics = Characteristics(**{"dexterity": 30, "MP": 140})


class Warrior(Character):
    # Класс Воина — ближний боец, основной урон зависит от силы (strength)
    def __init__(
        self,
        name: str,
        weapon: Weapon,
        armor: Armor,
        characteristics: Characteristics = warriorChar
    ) -> None:
        super().__init__(name, weapon, armor, characteristics)
        self.className: str = "Warrior"
        self.mainStat: int = self.strength

    @property
    def attackDamage(self) -> int:
        # Урон атаки воина: 2*сила + урон оружия
        return self.mainStat * 2 + self.weapon.weaponDmg


class Archer(Warrior):
    """
    Класс Лучника — дальний боец, основной урон зависит от ловкости (dexterity)
    Наследуется от Warrior, переопределяем mainStat
    """
    def __init__(
        self,
        name: str,
        weapon: Weapon,
        armor: Armor,
        characteristics: Characteristics = archerChar
    ) -> None:
        super().__init__(name, weapon, armor, characteristics)
        self.className: str = "Archer"
        self.mainStat: int = self.dexterity


class Mage(Character):
    """
    Класс Мага — заклинатель, использует магические атаки и медитацию для восстановления маны
    Атрибуты:
        mageSpells (Dict[str, MageSpell]): Доступные атакующие заклинания
        abilities (Dict[str, Ability]): Специальные способности (медитация)
    """
    def __init__(
        self,
        name: str,
        weapon: Weapon,
        armor: Armor,
        characteristics: Characteristics = mageChar
    ) -> None:
        super().__init__(name, weapon, armor, characteristics)
        self.className: str = "Mage"
        self.mageSpells: dict[str, MageSpell] = spells.mageSpells
        self.abilities: dict[str, Any] = abilities.mageAbilities

    def castSpell(self, target: Character, spell: MageSpell) -> None:
        """
        Применяет атакующее заклинание на цель
        Урон = базовый урон заклинания + 2*интеллект
        Расходует MP
        """
        damage: int = spell.dmg + self.intelligence * 2
        self.MP -= spell.costMP
        print(f'{self.name} использовал {spell.spellName} и нанес {getattr(target, "name")} магический урон {damage}')
        target.takeMageDamage(damage)

    def makeMove(self, targets: List[Character]) -> Optional[int]:
        """
        Логика хода мага:
          Если есть достаточно MP — использует самое дорогое заклинание
          Иначе — самое дешёвое
          Если MP не хватает даже на дешёвое — медитирует
        """
        if not(self.isAlive):
            print(f'{self.name} не может продолжать бой')
            return 0
        if len(targets) == 0:
            print("Все противники уже мертвы")
            return 

        target = random.choice(targets)
        if not(target.isAlive):
            print(f'{target.name} уже мертв, {self.name} не любит пинать труп')
            return 0

        # Находим самое дорогое и самое дешёвое заклинания
        max_expensive: MageSpell = max(self.mageSpells.values(), key=lambda s: s.costMP)
        min_expensive: MageSpell = min(self.mageSpells.values(), key=lambda s: s.costMP)

        if self.MP >= max_expensive.costMP:
            self.castSpell(target, max_expensive)
        elif self.MP >= min_expensive.costMP:
            self.castSpell(target, min_expensive)
        else:
            self.abilities["meditation"].effect(self)
            print(f'{self.name} использует медитацию и восполняет MP на 120 единиц маны')
        return None


class Healer(Mage):
    """
    Класс Хиллера — поддержка, использует лечебные заклинания и медитацию
    Переопределяет mageSpells и логику хода под лечение союзников
    """
    def __init__(
        self,
        name: str,
        weapon: Weapon,
        armor: Armor,
        characteristics: Characteristics = healChar
    ) -> None:
        super().__init__(name, weapon, armor, characteristics)
        self.className: str = "Healer"
        self.mageSpells: dict[str, HealSpell] = spells.healSpells
        self.abilities: dict[str, Any] = abilities.healerAbilities

    def castSpell(self, target: Character, spell: HealSpell) -> None:
        """
        Применяет лечебное заклинание
        Для массового лечения сообщение печатается отдельно
        """
        heal: int = spell.heal
        if spell.spellName != 'massHeal':
            print(f'{self.name} использует {spell.spellName} на {target.name}')
        target.takeHeal(heal)

    def makeMove(self, targets: List[Character]) -> None:
        """
        Логика хода целителя:
          Если все здоровы — медитирует
          Если много тяжелораненых — массовое лечение
          Иначе — лечит самого раненого доступным заклинанием
        """
        if len(targets) == 0:
            print("Все мертвы")
            return

        # Рассчитываем недостающее здоровье и процент повреждений
        injuries: List[int] = [(person.maxHP - person.HP) for person in targets]
        injuriesPercent: List[int] = [((person.maxHP - person.HP) * 100 // person.maxHP) for person in targets]
        seriouslyWounded: int = sum(1 for percent in injuriesPercent if percent > 70)
        mostWounded: int = max(injuries)

        if sum(injuries) == 0:
            self.abilities["meditation"].effect(self)
            print(f'У всех персонажей максимальное хп, поэтому {self.name} использует медитацию и восполняет MP на 50 единиц маны')
        elif (
            (all(person.HP < person.maxHP * 0.7 for person in targets) or seriouslyWounded >= len(targets) / 2)
            and self.MP > self.mageSpells["massHeal"].costMP
        ):
            print(f'{self.name} использует {self.mageSpells["massHeal"].spellName} на всех')
            self.MP -= self.mageSpells["massHeal"].costMP
            for target in targets:
                self.castSpell(target, self.mageSpells["massHeal"])
        elif self.MP > self.mageSpells["heal"].costMP:
            if mostWounded <= self.mageSpells["heal"].heal:
                self.castSpell(targets[injuries.index(mostWounded)], self.mageSpells["heal"])
                self.MP -= self.mageSpells["heal"].costMP
            elif self.MP > self.mageSpells["greatHeal"].costMP:
                self.castSpell(targets[injuries.index(mostWounded)], self.mageSpells["greatHeal"])
                self.MP -= self.mageSpells["greatHeal"].costMP
            else:
                self.castSpell(targets[injuries.index(mostWounded)], self.mageSpells["heal"])
                self.MP -= self.mageSpells["heal"].costMP
        else:
            self.abilities["meditation"].effect(self)
            print(f'{self.name} использует медитацию и восполняет MP на 50 единиц маны')