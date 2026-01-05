from typing import Callable, Any, Union


class Ability:
    """
    Класс, представляющий способность (умение) персонажа или босса.
    Атрибуты:
        nameAbility: Название способности
        effect: Функция, реализующая эффект способности
    """
    def __init__(self, nameAbility: str, effect: Callable) -> None:
        self.nameAbility = nameAbility
        self.effect = effect


class Abilities:
    """
    Контейнер для хранения способностей, разделённых по типам персонажей и боссов.
    Атрибуты:
        warriorAbilities (dict[str, Ability]) = {} - способности воина
        archerAbilities (dict[str, Ability]) = {} - способности лучника
        mageAbilities (dict[str, Ability]) = {} - способности мага
        healerAbilities (dict[str, Ability]) = {} - способности целителя
        bossAbilities (dict[str, Ability]) = {} - способности босса
    """
    def __init__(self) -> None:
        self.warriorAbilities: dict[str, Ability] = {}
        self.archerAbilities: dict[str, Ability] = {}
        self.mageAbilities: dict[str, Ability] = {}
        self.healerAbilities: dict[str, Ability] = {}
        self.bossAbilities: dict[str, Ability] = {}

    def addWarriorAbility(self, ability: Ability) -> None:
        # Добавляет способность в список способностей воина
        self.warriorAbilities[ability.nameAbility] = ability

    def addArcherAbility(self, ability: Ability) -> None:
        # Добавляет способность в список способностей лучника
        self.archerAbilities[ability.nameAbility] = ability

    def addMageAbility(self, ability: Ability) -> None:
        # Добавляет способность в список способностей мага
        self.mageAbilities[ability.nameAbility] = ability

    def addHealerAbility(self, ability: Ability) -> None:
        # Добавляет способность в список способностей целителя
        self.healerAbilities[ability.nameAbility] = ability

    def addBossAbility(self, ability: Ability) -> None:
        # Добавляет способность в список способностей босса
        self.bossAbilities[ability.nameAbility] = ability


# Глобальный словарь всех доступных способностей
allAbilities: dict[str, Ability] = {
    # Способность "медитация": восстанавливает 120 MP цели
    'meditation': Ability("meditation", lambda target: setattr(target, "MP", target.MP + 120)),
    # Способность "массовая атака": наносит урон всем целям из переданного списка
    'massAtack': Ability("massAtack", lambda targets, damage: [target.takePhysicalDamage(damage) for target in targets])
}

# Экземпляр контейнера способностей
abilities = Abilities()

# Назначение способностей конкретным ролям:
abilities.addHealerAbility(allAbilities['meditation'])
abilities.addMageAbility(allAbilities["meditation"])
abilities.addBossAbility(allAbilities["massAtack"])     