import random
from typing import Dict, List, Any, Optional
from bosses import bigBoss
from foes import Foe, Ghost, Sphinx, Wolf, Zombie
from foe_names import wolfName, ghostName, zombieName, sphinxName


class Location:
    """
    Представляет игровую локацию с описанием и списком врагов
    Атрибуты:
        title (str): Название локации
        description (str): Описание локации для вывода игроку
    """
    def __init__(self, title: str, description: str) -> None:
        self.title = title
        self.description = description

    @property
    def foes(self) -> List[Foe]:
        """
        Возвращает список врагов, соответствующих типу локации
        Для боссовой локации возвращает самого босса (bigBoss)
        """
        match self.title:
            case "forest":
                return [Wolf(name) for name in wolfName]
            case "haunted village":
                return [Ghost(name) for name in ghostName]
            case "burial ground":
                return [Zombie(name) for name in zombieName]
            case "piramids":
                return [Sphinx(name) for name in sphinxName]
            case "sinister castle":
                return [bigBoss]
            case _:
                raise ValueError(f"Неизвестная локация: {self.title}")
        return []

    def introduce(self) -> None:
        # Выводит описание локации и список врагов
        print(self.description)
        if self.foes:
            # Получаем тип врага (например, "волк") из первого врага
            foe_type: str = getattr(self.foes[0], "type")
            names: str = ", ".join(foe.getName() for foe in self.foes)
            print(f"Перед вами {len(self.foes)} {foe_type}: {names}")


class Locations:
    """
    Контейнер для управления доступными локациями
    Атрибуты:
        locations (Dict[str, Location]): Обычные игровые локации
        bossLocations (Dict[str, Location]): Локации боссов
        previousLocation (Optional[Location]): Последняя посещённая локация 
    """
    def __init__(self) -> None:
        self.locations: Dict[str, Location] = {}
        self.bossLocations: Dict[str, Location] = {
            "sinister castle": Location(
                "sinister castle",
                "И вот перед вами оказывается огромный зловещий замок"
            )
        }
        self.previousLocation: Optional[Location] = None

    def addLocation(self, location: Location) -> None:
        # Добавляет локацию в реестр доступных
        self.locations[location.title] = location

    def getLocations(self) -> Dict[str, Location]:
        """
        Возвращает словарь из 3 доступных локаций, исключая предыдущую
        Если предыдущей локации нет — удаляется случайная локация
        """
        if len(self.locations) == 0:
            raise Exception("Локации недоступны")

        locs: Dict[str, Location] = self.locations.copy()

        if self.previousLocation:
            # Удаляем предыдущую локацию из выбора
            if self.previousLocation.title in locs:
                del locs[self.previousLocation.title]
        else:
            index = random.choice(list(locs.keys()))
            del locs[index]
        return locs

    def setPreviousLoc(self, title: Optional[str]) -> None:
        # Устанавливает предыдущую локацию по её названию
        if not title:
            return
        if title in self.locations:
            self.previousLocation = self.locations[title]

    def getBossLocation(self) -> Location:
        # Возвращает локацию босса
        return self.bossLocations["sinister castle"]


# Инициализация глобального объекта локаций
locations = Locations()
locations.addLocation(Location("forest", "И вот вы дошли до темного леса"))
locations.addLocation(Location("haunted village", "Пройдя туда, вы попадаете в деревню, наполненную приведениями"))
locations.addLocation(Location("burial ground", "Вы шли в тумане и не заметили, как забрели на кладбище"))
locations.addLocation(Location("piramids", "Вы попали в заброшенную подземную пирамиду"))