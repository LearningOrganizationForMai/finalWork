import random
import time
from typing import List, Dict, Any, Optional, Union
from artifacts import artifacts
from auth import auth
import globals
from locations import locations
from party import createPartyFromSave, getArtifacts, defaultParty
from save import create_save_data, load_save, save_save
from bosses import bigBoss


def round(start: int, party: List[Any], loadData: Dict[str, Any]) -> str:
    """
    Основной игровой цикл: прохождение локаций до финального боя с боссом
    Аргументы:
        start (int): Начальный этап (stage)
        party (List[Character]): Список живых персонажей
        loadData (Dict): Данные из сохранения
    Возвращает:
        "Выход" — если игрок выбрал выйти
    """
    for globals.STAGE in range(start, globals.STAGE_LIMIT + 1):
        # Получаем три случайные локации
        loc: Dict[str, Any] = locations.getLocations()
        keys: List[str] = list(loc.keys())
        # Игрок выбирает одну из трёх локаций
        chooseLoc: int = int(input(f"""Перед вами открываются 3 дороги. 
                Справа возвышается {keys[0]}, если вы хотите пойти туда введите 1. 
                Спереди вы видите {keys[1]}, если вы хотите пойти туда введите 2. 
                Слева располагается {keys[2]}, если вы хотите пойти туда введите 3.             
                """))
        # Валидация, чтобы ввели 1/2/3
        while chooseLoc not in (1, 2, 3):
            chooseLoc = int(input(f"""Перед вами открываются 3 дороги. 
                Справа возвышается {keys[0]}, если вы хотите пойти туда введите 1. 
                Спереди вы видите {keys[1]}, если вы хотите пойти туда введите 2. 
                Слева располагается {keys[2]}, если вы хотите пойти туда введите 3.             
                """))

        print(f"Вы пошли к локации: {loc[keys[chooseLoc - 1]].title}")
        curLocation = loc[keys[chooseLoc - 1]]
        locations.setPreviousLoc(curLocation.title)
        curLocation.introduce()

        # Начало боя с врагами на локации
        foes: List[Any] = curLocation.foes
        battle(party, foes)

        # Убираем мёртвых из отряда
        party = [character for character in party if character.isAlive]

        # Сохранение прогресса
        saveData: Dict[str, Any] = create_save_data(party, locations.previousLocation, loadData)
        save_save(saveData)
        print("Данные сохранены")

        # Предложение выйти из игры
        message: str = input("Хотите ли выйти? Да/Нет ")
        while message not in ("Да", "Нет"):
            message = input("Хотите ли выйти? Да/Нет ")
        if message == "Да":
            return "Выход"

    # Финальная локация — бой с боссом
    loc = locations.getBossLocation()
    loc.introduce()
    foes = [bigBoss]
    globals.STAGE = 1  # Сброс этапа после победы
    partyState: str = battle(party, foes)
    party[:] = [character for character in party if character.isAlive]
    saveData = create_save_data(party, locations.previousLocation, loadData)
    save_save(saveData)
    print("Данные сохранены")
    print("Вы завершили испытание, ваши итоги: ")
    print(f"Остались в живых: {partyState}")
    return None


def game() -> None:
    # Точка входа в игру: аутентификация, загрузка или начало новой игры
    # Аутентификация пользователя
    while globals.USER is None:
        auth()

    # Загрузка сохранённых данных
    loadData: Dict[str, Any] = load_save()
    loadedPreviousLocation: Optional[str] = None

    if str(globals.USER) in loadData and len(loadData[str(globals.USER)]["party"]) > 0:
        party: List[Any] = createPartyFromSave(loadData[str(globals.USER)]["party"])
        loadedPreviousLocation = loadData[str(globals.USER)]["previousLocation"]
        globals.STAGE = loadData[str(globals.USER)]["stage"] + 1
    else:
        party = defaultParty

    # Выбор действия: продолжить, новая игра или выход
    varinat: str = input("Для продолжения игры, напишите continue, для новой игры напишите new game, для выхода из игры напишите выход\n")
    while varinat not in ("continue", "new game", "выход"):
        varinat = input("Вы ввели некорректный ответ. Ответьте: continue/new game/выход \n")

    # Продолжение сохранённой игры
    if varinat == "continue":
        print("Загрузка ваших данных")
        time.sleep(1)
        start: int = globals.STAGE
        locations.setPreviousLoc(loadedPreviousLocation)
        round(start, party, loadData)

    # Начало новой игры
    elif varinat == "new game":
        party = defaultParty
        print("Запускаем новую игру")
        time.sleep(0.5)
        globals.STAGE = 1
        start = globals.STAGE
        round(start, party, loadData)

    # Выход
    else:
        print("Ждем вас еще")
        return


def battle(party: List[Any], foes: List[Any]) -> str:
    """
    Система боя: инициатива по ловкости, ходы по очереди, обновление очереди после смертей
    Возвращает строку с итоговым состоянием отряда
    """
    battlers: List[Any] = party + foes
    # Сортировка по ловкости в порядке убывания
    queue: List[Any] = sorted(battlers, key=lambda person: person.dexterity, reverse=True)

    while len(party) > 0 and len(foes) > 0:
        for person in queue:
            if not person.isAlive:
                continue
            # Персонажи атакуют врагов, а Healer лечат отряд
            if person.className in ("Warrior", "Archer", "Mage"):
                person.makeMove(foes)
            else:
                person.makeMove(party)

            # Обновление списков живых
            party = [character for character in party if character.isAlive]
            foes = [foe for foe in foes if foe.isAlive]

            # Если состав боя изменился — пересчитываем очередь
            if len(party) + len(foes) != len(queue):
                battlers = party + foes
                queue = sorted(battlers, key=lambda p: p.dexterity, reverse=True)
                break  # завершаем текущий раунд, начинаем новый с обновлённой очередью

        # Формирование отчёта о состоянии боя
        if party:
            partyState: str = "\n".join(f"{character.name} имеет {character.HP} HP, {character.MP} MP" for character in party)
        else:
            partyState = "К сожалению все погибли"

        if foes:
            foeState: str = "\n".join(f"{foe.name} имеет {foe.HP} HP" for foe in foes)
        else:
            foeState = "Все мертвы"

        print(f"На данный момент состояние персонажей: {partyState}")
        print(f"На данный момент состояние противников: {foeState}")
        print('Нажмите enter, чтобы сделать следующий ход')
        input()

    # Выпадение артефакта после победы
    partyArtifacts: List[str] = []
    for character in party:
        partyArtifacts.extend(character.showArtifacts())

    allArtifacts: List[Dict[str, str]] = artifacts.showAllArtifacts()
    avalibleArtifacts: List[str] = []

    # Ограничение на количество копий одного артефакта
    for art in allArtifacts:
        if partyArtifacts.count(art["artifactName"]) < len(partyArtifacts) // 12 + 1:
            avalibleArtifacts.append(art["artifactName"])

    if avalibleArtifacts:
        droppedArtifact = artifacts.getArtifact(random.choice(avalibleArtifacts))
        print(f"Пройдя локацию вы натыкаетесь на {getattr(droppedArtifact, 'artifactName')}")
        # Артефакт получает персонаж, соответствующий по классу
        for person in party:
            if getattr(person, "className").lower() == getattr(droppedArtifact, "className"):
                person.getArtifact(droppedArtifact)

    return partyState