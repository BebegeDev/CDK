from pvlib.location import Location
import pandas as pd
import datetime


class SolarModelStandbyMode:
    """SolarModelStandbyMode - класс предназначенный для определения поведения фотоэлектрических модулей
    на основе библиотеки pvlib, если основной режим выйдет из строя.
     Класс будет определять географическое положение объекта, за счет этого определять позицию солнца на небе
      в разное время суток, а также интенсивность солнечного излучения.
    """

    def __init__(self, latitude, longitude, loc, altitude, name):
        self.latitude = latitude
        self.longitude = longitude
        # определение местоположения
        self.loc = Location(latitude, longitude, loc, altitude, name)  # определение локализации
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)  # опр-ие завтрашнего дня
        times = pd.date_range(start=datetime.date.today(), end=tomorrow, freq="1Min")  # разбиение суток поминутно (
        self.times = times.tz_localize(self.loc.pytz)  # локализация места с временем

    @staticmethod
    def solar_position(f, arr):  # для определения местоположения солнца и прихода радиации
        # условие работы зависит от приходящей функции
        spa_out = f(*arr)
        return spa_out
