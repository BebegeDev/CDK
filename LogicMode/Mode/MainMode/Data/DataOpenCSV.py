import csv
import pandas as pd


class DataCSV:
    """ DataCSV - класс предназначенный для получения данных в настоящий момент времени.
     Класс будет иметь связь между БД разного типа.
     Переменная БД - хранит фактические значения в настоящее время.

     Метод __init__ - инициализация класса. Реализует связь между БД и классом.
     Метод data - метод получения массива значений из БД.
    """

    def __init__(self, key):
        self._data = []
        self.key = key

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data_fact):
        with open(data_fact) as file:
            rows = csv.reader(file, delimiter=self.key)
            count = True
            list_data = []
            for row in rows:
                if count:
                    name = row
                    count = False
                else:
                    list_data.append(row)
            self._data.append(pd.concat([pd.DataFrame(list_data, columns=name)], ignore_index=True))






