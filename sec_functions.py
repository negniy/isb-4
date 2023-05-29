import hashlib
import logging
import json

def check_hash(card_center: int, card_begin: int) -> int:
    """Функция делает проверку хэша по номеру карты

    Args:
        card_center (int): середина номера карты
        card_begin (int): начало номера карты

    Returns:
        int: номер, если проверка пройдена, и False в противном случае
    """
    with open("setting.json", "r") as read_file:
        SETTING = json.load(read_file)
    logging.info("Проверка хеша")
    card_number = str(card_begin) + str(card_center) + SETTING['last_digits']
    card_hash = hashlib.sha1((card_number).encode()).hexdigest()
    return card_number if SETTING['hash'] == card_hash else False


def algorithm_luna(card_number: str) -> bool:
    """Функция проверки номера карты алгоритмом Луна

    Args:
        card_number (str): номер карты

    Returns:
        bool: булевское значение результата проверки(прошел/не прошел)
    """
    check = 7
    all_number = list(map(int, card_number))
    all_number = all_number[::-1]
    for i, num in enumerate(all_number):
        if i % 2 == 0:
            tmp = num*2
            if tmp > 9:
                tmp -= 9
            all_number[i] = tmp
    total_sum = sum(all_number)
    rem = total_sum % 10
    check_sum = 10 - rem if rem != 0 else 0
    return True if check_sum == check else False