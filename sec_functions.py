import hashlib
import logging

SETTING = {
    'hash': '754a917a9c82f5247412006a5abe1c0eb76e1007',
    'begin_digits': ['529460', '519998', '529025','5156451','522327','522329','523760','527652','528528','529158','529856','530176','531855','534133','518591','528154','526589','510144','532465','531456','531452','531963','534299','540989','530429','531866','534135','518640'],
    'last_digits': '0758',
}

def check_hash(card_center: int, card_begin: int) -> int:
    """Функция делает проверку хэша по номеру карты

    Args:
        card_center (int): середина номера карты
        card_begin (int): начало номера карты

    Returns:
        int: номер, если проверка пройдена, и False в противном случае
    """
    logging.info("Проверка хеша")
    card_number = str(card_begin) + str(card_center) + SETTING['last_digits']
    card_hash = hashlib.sha1(card_number.encode()).hexdigest()
    if SETTING['hash'] == card_hash:
        return card_number
    return False


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
    if rem != 0:
        check_sum = 10 - rem
    else:
        check_sum = 0
    return True if check_sum == check else False