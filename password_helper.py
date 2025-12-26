import os
import random
import string
import getpass
from cryptography.fernet import Fernet

# Функция для загрузки или создания ключа шифрования
def zagruzit_klyuch():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    else:
        klyuch = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(klyuch)
        return klyuch

# Функция для сохранения пароля в зашифрованном виде
def sokhranit_parol(servis, parol):
    klyuch = zagruzit_klyuch()
    f = Fernet(klyuch)
    
    if os.path.exists("passwords.txt"):
        with open("passwords.txt", "rb") as file:
            zashifrovanno = file.read()
        if zashifrovanno:
            staraya_infa = f.decrypt(zashifrovanno).decode()
        else:
            staraya_infa = ""
    else:
        staraya_infa = ""

    # Проверим, не существует ли уже такой сервис
    stroki = staraya_infa.strip().split('\n') if staraya_infa.strip() else []
    novye_stroki = []
    naydeno = False
    for stroka in stroki:
        if stroka.startswith(servis + ":"):
            novye_stroki.append(f"{servis}: {parol}")
            naydeno = True
        else:
            novye_stroki.append(stroka)
    if not naydeno:
        novye_stroki.append(f"{servis}: {parol}")
    
    vsya_infa = "\n".join(novye_stroki) + "\n"

    zashifrovannaya_infa = f.encrypt(vsya_infa.encode())
    with open("passwords.txt", "wb") as file:
        file.write(zashifrovannaya_infa)
    print("Пароль сохранен!")

# Функция для отображения всех сохраненных паролей
def pokazat_paroli():
    if not os.path.exists("passwords.txt"):
        print("Нет сохраненных паролей.")
        return
    klyuch = zagruzit_klyuch()
    f = Fernet(klyuch)
    with open("passwords.txt", "rb") as file:
        zashifrovanno = file.read()
    if not zashifrovanno:
        print("Нет сохраненных паролей.")
        return
    try:
        rasshifrovanno = f.decrypt(zashifrovanno).decode()
        print("\nВаши пароли:")
        print(rasshifrovanno.strip())
    except Exception:
        print("Не удалось расшифровать. Возможно, файл поврежден.")

#Получить пароль по названию сервиса
def poluchit_parol_po_servisu():
    if not os.path.exists("passwords.txt"):
        print("Нет сохраненных паролей.")
        return
    klyuch = zagruzit_klyuch()
    f = Fernet(klyuch)
    with open("passwords.txt", "rb") as file:
        zashifrovanno = file.read()
    if not zashifrovanno:
        print("Нет сохраненных паролей.")
        return
    try:
        rasshifrovanno = f.decrypt(zashifrovanno).decode()
    except Exception:
        print("Не удалось расшифровать. Возможно, файл поврежден.")
        return

    servis = input("Введите название сервиса: ").strip()
    if not servis:
        print("Название сервиса не может быть пустым.")
        return

    stroki = rasshifrovanno.strip().split('\n')
    for stroka in stroki:
        if stroka.startswith(servis + ":"):
            chast = stroka.split(": ", 1)
            if len(chast) == 2:
                nuzhnyy_parol = chast[1]
                print(f"\nПароль для '{servis}': {nuzhnyy_parol}")
                print("Скопируйте его вручную (выделите и нажмите Ctrl+C).")
                return
    print(f"Пароль для сервиса '{servis}' не найден.")

# Функция для генерации нового пароля
def sozdat_parol():
    print("\nНастройка генератора пароля")
    dlina = input("Длина пароля (по умолчанию 12): ").strip()
    if not dlina.isdigit():
        dlina = 12
    else:
        dlina = int(dlina)
    if dlina < 4:
        dlina = 4

    dobavit_tsifry = input("Добавить цифры? (да/нет): ").lower() == "да"
    dobavit_zaglavnye = input("Добавить заглавные буквы? (да/нет): ").lower() == "да"
    dobavit_simvoly = input("Добавить символы (!@#$%)? (да/нет): ").lower() == "да"
    ubrat_pokhozhie = input("Убрать похожие символы (l, 1, O, 0)? (да/нет): ").lower() == "да"

    simvoly = ""
    if dobavit_tsifry:
        simvoly += string.digits
    if dobavit_zaglavnye:
        simvoly += string.ascii_uppercase
    simvoly += string.ascii_lowercase
    if dobavit_simvoly:
        simvoly += "!@#$%"

    if ubrat_pokhozhie:
        for plokhoi in "l1O0":
            simvoly = simvoly.replace(plokhoi, "")

    if not simvoly:
        simvoly = string.ascii_lowercase

    novyy_parol = ''.join(random.choice(simvoly) for _ in range(dlina))
    print(f"\nВаш пароль: {novyy_parol}")
    return novyy_parol

# Функция для проверки надежности пароля
def proverit_nadzhnost(parol):
    ochki = 0
    if len(parol) >= 8:
        ochki += 1
    if any(c.islower() for c in parol):
        ochki += 1
    if any(c.isupper() for c in parol):
        ochki += 1
    if any(c.isdigit() for c in parol):
        ochki += 1
    if any(c in "!@#$%" for c in parol):
        ochki += 1

    if ochki == 5:
        return "Очень надежный"
    elif ochki >= 3:
        return "Средний"
    else:
        return "Слабый"

# Основная функция с меню
def main():
    print("Простой менеджер паролей")
    while True:
        print("\nЧто вы хотите сделать?")
        print("1. Создать пароль")
        print("2. Проверить пароль на надежность")
        print("3. Сохранить пароль")
        print("4. Показать все пароли")
        print("5. Получить пароль по названию")
        print("6. Выйти")

        vibor = input("Введите номер действия: ").strip()

        if vibor == "1":
            parol = sozdat_parol()
            print("Оценка:", proverit_nadzhnost(parol))

        elif vibor == "2":
            parol = getpass.getpass("Введите пароль для проверки (он не отображается): ")
            if parol:
                print("Оценка:", proverit_nadzhnost(parol))
            else:
                print("Пароль не введен.")

        elif vibor == "3":
            servis = input("Название сервиса: ").strip()
            if not servis:
                print("Название не может быть пустым!")
                continue
            parol = getpass.getpass("Пароль (не отображается): ")
            if not parol:
                print("Пароль не введен!")
                continue
            sokhranit_parol(servis, parol)

        elif vibor == "4":
            pokazat_paroli()

        elif vibor == "5":
            poluchit_parol_po_servisu()

        elif vibor == "6":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()


