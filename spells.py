from typing import Dict


class Spell:
    """
    Базовый класс для всех заклинаний
    Атрибуты:
        spellName (str): Название заклинания
        costMP (int): Стоимость MP
    """
    def __init__(self, spellName: str, costMP: int) -> None:
        self.spellName = spellName
        self.costMP = costMP


class MageSpell(Spell):
    """
    Атакующее заклинание мага
    Дополнительный атрибут:
        dmg (int): Наносимый магический урон
    """
    def __init__(self, spellName: str, costMP: int, dmg: int) -> None:
        super().__init__(spellName, costMP)
        self.dmg = dmg


class HealSpell(Spell):
    """
    Лечебное заклинание (используется целителем)
    Дополнительный атрибут:
        heal (int): Восстанавливаемое количество HP
    """
    def __init__(self, spellName: str, costMP: int, heal: int) -> None:
        super().__init__(spellName, costMP)
        self.heal = heal


class Spells:
    """
    Контейнер для хранения заклинаний, разделённых по типу:
      атакующие для мага
      лечебные для целителя
    Атрибуты:
        mageSpells (Dict[str, MageSpell]): Словарь атакующих заклинаний
        healSpells (Dict[str, HealSpell]): Словарь лечебных заклинаний
    """
    def __init__(self) -> None:
        self.mageSpells: Dict[str, MageSpell] = {}
        self.healSpells: Dict[str, HealSpell] = {}

    def addMageSpell(self, mageSpell: MageSpell) -> None:
        # Добавляет атакующее заклинание в реестр мага
        self.mageSpells[mageSpell.spellName] = mageSpell

    def addHealSpell(self, healSpell: HealSpell) -> None:
        # Добавляет лечебное заклинание в реестр целителя
        self.healSpells[healSpell.spellName] = healSpell


# Предопределённые заклинания
mageSpells = {
    "fireball": MageSpell("fireball", 60, 40),   # Мощный огненный шар
    "scorch": MageSpell("scorch", 30, 20)        # Быстрое, но слабое пламя
}

healSpells = {
    "greatHeal": HealSpell("greatHeal", 60, 80), # Сильное лечение одной цели
    "heal": HealSpell("heal", 30, 40),           # Базовое лечение
    "massHeal": HealSpell("massHeal", 45, 35)    # Массовое лечение всех союзников
}


# Инициализация глобального реестра заклинаний
spells = Spells()

# Регистрация атакующих заклинаний
for i in mageSpells:
    spells.addMageSpell(mageSpells[i])

# Регистрация лечебных заклинаний
for i in healSpells:
    spells.addHealSpell(healSpells[i])