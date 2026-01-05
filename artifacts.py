from dataclasses import dataclass, field
from typing import Literal, Dict, Any, Optional, List


class Artifact:
    """
    Артефакт — уникальный предмет, привязанный к определённому классу персонажа
    Атрибуты:
        artifactName (str): Название артефакта
        className (str): Имя класса, к которому привязан артефакт
    """
    def __init__(self, artifactName: str, className: str) -> None:
        self.artifactName = artifactName
        self.className = className


class Artifacts:
    """
    Контейнер для хранения артефактов, разделённых по классам персонажей
    Атрибуты:
        warrior (Dict[str, Artifact]): Артефакты для воина
        archer (Dict[str, Artifact]): Артефакты для лучника
        mage (Dict[str, Artifact]): Артефакты для мага
        healer (Dict[str, Artifact]): Артефакты для целителя
    """
    def __init__(self) -> None:
        self.warrior: dict[str, Artifact] = {}
        self.archer: dict[str, Artifact] = {}
        self.mage: dict[str, Artifact] = {}
        self.healer: dict[str, Artifact] = {}

    def addWarriorArtifact(self, artifact: Artifact) -> None:
        # Добавляет артефакт в коллекцию артефактов воина
        self.warrior[artifact.artifactName] = artifact

    def addArcherArtifact(self, artifact: Artifact) -> None:
        # Добавляет артефакт в коллекцию артефактов лучника
        self.archer[artifact.artifactName] = artifact

    def addMageArtifact(self, artifact: Artifact) -> None:
        # Добавляет артефакт в коллекцию артефактов мага
        self.mage[artifact.artifactName] = artifact

    def addHealerArtifact(self, artifact: Artifact) -> None:
        # Добавляет артефакт в коллекцию артефактов целителя
        self.healer[artifact.artifactName] = artifact

    def getArtifact(self, artName: str) -> Optional[Artifact]:
        """
        Ищет артефакт по его имени
        Возвращает:
            Artifact — если найден
            None — если не найден
        """
        for className in self.__dict__:
            # Пропускаем атрибуты, не являющиеся словарями артефактов
            if not isinstance(getattr(self, className), dict):
                continue
            for art in getattr(self, className).values():
                if art.artifactName == artName:
                    return art

    def showAllArtifacts(self) -> List[Dict[str, str]]:
        # Возвращает список всех артефактов в виде словарей с полями 'artifactName' и 'className'
        artifacts: List[Dict[str, str]] = []
        for art in self.warrior.values():
            artifacts.append({"artifactName": art.artifactName, "className": art.className})
        for art in self.archer.values():
            artifacts.append({"artifactName": art.artifactName, "className": art.className})
        for art in self.mage.values():
            artifacts.append({"artifactName": art.artifactName, "className": art.className})
        for art in self.healer.values():
            artifacts.append({"artifactName": art.artifactName, "className": art.className})
        return artifacts


warriorArtifacts = {
    "steel underwear": Artifact("steel underwear", "warrior"),
    "thongs of virtue": Artifact("thongs of virtue", "warrior"),
    "borat Mankini": Artifact("borat Mankini", "warrior")
}

archerArtifact = {
    "rocktlauncher": Artifact("rocktlauncher", "archer"),
    "railgun": Artifact("railgun", "archer"),
    "bfg9000": Artifact("bfg9000", "archer")
}

mageArtifact = {
    "medved": Artifact("medved", "mage"),
    "vodka": Artifact("vodka", "mage"),
    "balalaika": Artifact("balalaika", "mage")
}

healerArtifact = {
    "kigurumi": Artifact("kigurumi", "healer"),
    "dakimakura": Artifact("dakimakura", "healer"),
    "maneki-neko": Artifact("maneki-neko", "healer")
}


# Создание реестра артефактов и регистрация всех предметов
artifacts = Artifacts()

for artifact in warriorArtifacts.values():
    artifacts.addWarriorArtifact(artifact)

for artifact in archerArtifact.values():
    artifacts.addArcherArtifact(artifact)

for artifact in mageArtifact.values():
    artifacts.addMageArtifact(artifact)

for artifact in healerArtifact.values():
    artifacts.addHealerArtifact(artifact)

