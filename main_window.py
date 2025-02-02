import multiprocessing as mp
import json
import sys
import time
import re

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow,
                             QProgressBar, QPushButton)

from charting import charting
from sec_functions import algorithm_luna, check_hash


class Window(QMainWindow):
    def __init__(self) -> None:
        """Функция инициализации
        """
        super(Window, self).__init__()
        self.setWindowTitle('Поиск номера банковской карты')
        self.setFixedSize(600, 400)
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 600, 400)
        self.background.setPixmap(QPixmap("background.jpg").scaled(600, 400))
        self.info = QLabel(self)
        self.info.setText("Известная часть карты: **** **** **** 0758")
        self.info.setGeometry(150, 10, 300, 50)
        self.info1 = QLabel(self)
        self.info1.setText("Выберите BIN карты:")
        self.info1.setGeometry(25, 60, 250, 100)
        self.info2 = QLabel(self)
        self.info2.setText("Выберите кол-во потоков:")
        self.info2.setGeometry(25, 110, 250, 100)
        self.info2.hide()
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.progress.setGeometry(115, 250, 400, 50)
        self.progress.hide()
        self.button_card = QPushButton('Найти карту', self)
        self.button_card.setGeometry(200, 190, 200, 50)
        self.button_card.clicked.connect(self.find_card)
        self.button_card.hide()
        self.result = QLabel(self)
        self.result.setGeometry(150, 250, 400, 200)
        self.pool_size = QtWidgets.QComboBox(self)
        self.pool_size.addItems([str(i) for i in range(1, 33)])
        self.pool_size.setGeometry(200, 135, 200, 50)
        self.pool_size.hide()
        self.number = QtWidgets.QComboBox(self)
        self.number.addItems(SETTING["begin_digits"])
        self.number.setGeometry(200, 80, 200, 50)
        self.number.activated[str].connect(self.on_activated)
        self.graph = QPushButton('Построить график', self)
        self.graph.setGeometry(200, 245, 200, 50)
        self.graph.clicked.connect(self.show_graph)
        self.graph.hide()
        self.show()

    def on_activated(self, text: str) -> None:
        """Функция выбора BIN карты
        """
        self.graph.hide()
        self.pool_size.show()
        self.info2.show()
        try:
            self.number = int(re.findall('(\d+)', text)[0])
        except:
            self.number = SETTING['begin_digits'][0]
        self.pool_size.activated[str].connect(self.choose_pool)

    def choose_pool(self, text: str):
        """Функция выбора кол-ва потоков
        """
        try:
            self.size = int(re.findall('(\d+)', text)[0])
        except:
            self.size = 0
        self.button_card.show()

    def find_card(self, start: float) -> None:
        """Функция поиска карты

        Args:
            start (float): время начала поиска
        """
        item = [(i, self.number) for i in range(99999, 10000000)]
        start = time.time()
        self.progress.show()
        QApplication.processEvents()
        with mp.Pool(self.size) as p:
            for i, result in enumerate(p.starmap(check_hash, item)):
                if result:
                    self.success(start, result)
                    break
                self.progress.setValue(int((i)/9900000*100))
                QApplication.processEvents()
            else:
                self.result.setText('Не найдено')
                self.progress.setValue(0)
        self.progress.hide()

    def success(self, start: float, result: int):
        """Функция обновляет прогресс бар и выводит информацию о карте и времени поиска

        Args:
            start (float): время начала поиска
            result (int): времяя конца поиска
        """
        self.result_card = result
        self.progress.setValue(100)
        end = time.time() - start
        result_text = f'Расшифрованный номер: {result}\n'
        result_text += f'Проверка на алгоритм Луна: {algorithm_luna(result)}\n'
        result_text += f'Время: {end:.2f} секунд'
        self.result.setText(result_text)
        self.graph.show()

    def show_graph(self):
        """Функция отрисовки графика
        """
        charting(self.result_card)



if __name__ == "__main__":
    with open("setting.json", "r") as read_file:
        SETTING = json.load(read_file)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())