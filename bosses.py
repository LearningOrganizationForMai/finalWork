import random
from typing import List, Dict, Any
from character import Character, Characteristics
from weapon import weapons
from armor import armors
from abilities import abilities


# Предопределённые характеристики босса
bossChar: Characteristics = Characteristics(**{"maxHP": 1500, "HP": 1500, "strength": 30, "dexterity": 20})


class Boss(Character):
    """
    Класс босса — особый тип персонажа с фазами боя, специальными способностями и поведением
    Атрибуты:
        className (str): Тип класса — всегда "Boss"
        type (str): Подтип — "Big Boss"
        abilities (Dict[str, Ability]): Словарь способностей, доступных боссу
        phase (int): Текущая фаза боя (0 — начальная, 1–3 — последующие)
        massAtackCD (int): Текущий кулдаун до следующего использования массовой атаки
    """
    def __init__(
        self,
        name: str,
        weapon: Any = weapons.boss["cleaver"],
        armor: Any = armors.boss["bossArmor"],
        characteristics: Characteristics = bossChar
    ) -> None:
        super().__init__(name, weapon, armor, characteristics)
        self.className: str = "Boss"
        self.type: str = "Big Boss"
        self.abilities: Dict[str, Any] = abilities.bossAbilities
        self.phase: int = 0
        self.massAtackCD: int = 4 

    @property
    def attackDamage(self) -> int:
        """
        Вычисляет урон базовой атаки босса
        Формула: 50% от силы + урон оружия
        """
        return int(self.strength * 0.5) + self.weapon.weaponDmg

    def firtsPhase(self) -> None:  
        # Переход в первую фазу: босс меняет оружие на более мощное
        
        self.weapon = weapons.boss["hugeClub"]
        self.phase = 1
        print(f'{self.name} разозлился и достал новое оружие {self.weapon.weaponName}')

    def secondPhase(self) -> None:
        # Переход во вторую фазу: босс удваивает силу и сбрасывает кулдаун массовой атаки
        self.massAtackCD = 0
        self.strength *= 2
        self.phase = 2
        print(f'{self.name} впал в ярость и стал бить с силой {self.strength}')

    def thirdPhase(self) -> None:
        """
        Переход в третью фазу: босс резко увеличивает ловкость (возводит в квадрат)
        и начинает действовать быстрее всех.
        """
        self.massAtackCD = 0
        self.dexterity **= 2
        self.phase = 3
        print(f'{self.name} в отчаянии и начинает бить с максимальной скоростью, опережая всех остальных персонажей. \n' +
              f'Его скорость доросла до {self.dexterity}')

    def makeMove(self, targets: List[Any]) -> int:
        """
        Выполняет ход босса в бою
        Логика:
          Проверка жив ли босс
          Автоматический переход между фазами при падении HP
          Выбор цели и выполнение атаки или массовой атаки (в зависимости от фазы и кулдауна)
        Возвращает:
            0 — если босс мёртв
        """
        if not self.isAlive:
            print(f'{self.name} не может продолжать бой')
            return 0

        # Автоматическое переключение фаз при снижении HP
        if self.HP < self.maxHP * 0.7 and self.phase == 0:
            self.firtsPhase()
        elif self.HP < self.maxHP * 0.5 and self.phase == 1:
            self.secondPhase()
        elif self.HP < 0.3 * self.maxHP and self.phase == 2:
            self.thirdPhase()

        # Выбор случайной цели из списка
        target = random.choice(targets)

        if self.phase <= 1:
            self.attack(target)
            self.massAtackCD -= 1
        elif self.phase == 2:
            if self.massAtackCD <= 0:
                print(f'{self.name} яростно атакует всех')
                self.abilities["massAtack"].effect(targets, self.attackDamage)
                self.massAtackCD = 4
            else:
                self.attack(target)
                self.massAtackCD -= 1
        else:
            if self.massAtackCD <= 0:
                print(f'{self.name} яростно атакует всех')
                self.abilities["massAtack"].effect(targets, self.attackDamage)
                self.massAtackCD = 4
            else:
                self.attack(target)
                self.massAtackCD -= 2  # В третьей фазе кулдаун уменьшается быстрее

    def getName(self) -> str:
        # Возвращает имя босса
        return self.name


# Создание экземпляра босса с именем "Pudge"
bigBoss = Boss("Pudge")