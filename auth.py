from registration import login, registration
import time


def auth() -> None:
    """
    Функция аутентификации пользователя: предлагает войти в существующий аккаунт
    или зарегистрировать новый. Запрашивает логин и пароль, затем вызывает
    соответствующую функцию из модуля registration
    """
    # Запрос у пользователя, существует ли у него аккаунт
    checkAcc: str = input("У вас есть аккаунт? Да/Нет\n")
    
    # Валидация ввода
    while checkAcc != "Да" and checkAcc != "Нет":
        checkAcc = input("Вы ввели некорректный ответ. У вас есть аккаунт? Да/Нет\n")
    
    if checkAcc == 'Да':
        # Вход в существующий аккаунт
        playerlogin: str = input("Введите логин\n")
        playerpassword: str = input("Введите пароль\n")
        print("Загружаем данные")
        time.sleep(1)  # Эмуляция загрузки, чтобы выглядело лучше и не всплывало окно сразу
        login(playerlogin, playerpassword)
    else:
        # Регистрация нового аккаунта
        playerlogin = input("Придумайте себе логин\n")
        playerpassword = input("Придумайте себе пароль\n")
        print("Загружаем данные")
        time.sleep(1)  # Эмуляция загрузки, чтобы выглядело лучше и не всплывало окно сразу
        registration(playerlogin, playerpassword)