import multiprocessing as mp
import time

import matplotlib.pyplot as plt
import numpy as np

from sec_functions import check_hash


def charting(card_number: str):
    """Функция создания графика

    Args:
        card_number (str): номер карты
    """
    times = np.empty(shape=0)
    card_number = card_number[:6]
    items = [(i, card_number) for i in range(99999, 10000000)]
    for i in range(1, 8):
        start = time.time()
        with mp.Pool(i) as p:
            for i, result in enumerate(p.starmap(check_hash, items)):
                if result:
                    end = time.time() - start
                    times = np.append(times, end)
                    break
    plt.bar(range(len(times)), np.round(times, 2).tolist())
    plt.xlabel("Число потоков")
    plt.ylabel("Время, с")
    plt.title("Зависимость времени от числа потоков")
    plt.show()
