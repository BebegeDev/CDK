import csv
import pandas as pd
import pvlib.solarposition
from pvlib.location import Location
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS, sapm_cell
import datetime
import matplotlib.pyplot as plt


# ======================================================================================================================


class Data:
    """ Data - класс предназначенный для получения данных в настоящий момент времени.
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


# ======================================================================================================================


class EquipCondition:
    """ EquipCondition - родительский класс определяющий схожие параметры для оборудования СДК.
        Метод __init__ - инициализирует параметры присущие каждому оборудованию.
    """

    def __init__(self, voltage, frequency, current, power):
        self.voltage = voltage
        self.frequency = frequency
        self.current = current
        self.power = power


# ======================================================================================================================


class SolarEquip(EquipCondition):
    """ SolarEquip - дочерний класс определяющий дополнительные параметры СЭС.
        __init__ - инициализирует параметры присущие классу EquipCondition и дополнительные для СЭС.
    """

    def __init__(self, voltage, frequency, current, power, voltage_dc, voltage_ac, protocol):
        EquipCondition.__init__(self, voltage, frequency, current, power)
        self.voltage_DC = voltage_dc
        self.voltage_AC = voltage_ac
        self.protocol = protocol


# ======================================================================================================================


class DieselEquip(EquipCondition):
    """ DieselEquip - дочерний класс определяющий дополнительные параметры ДГУ.
        __init__ - инициализирует параметры присущие классу EquipCondition и дополнительные для ДГУ.
    """

    def __init__(self, voltage, frequency, current, power, frequency_shaft, fuel_consumption):
        EquipCondition.__init__(self, voltage, frequency, current, power)
        self.frequency_shaft = frequency_shaft
        self.fuel_consumption = fuel_consumption


# ======================================================================================================================


class StorageEquip(EquipCondition):
    """ StorageEquip - дочерний класс определяющий дополнительные параметры СЭН.
        __init__ - инициализирует параметры присущие классу EquipCondition и дополнительные для СЭН.
    """

    def __init__(self, voltage, frequency, current, power, voltage_dc, voltage_ac, current_discharge, discharge,
                 capacity):
        EquipCondition.__init__(self, voltage, frequency, current, power)
        self.voltage_DC = voltage_dc
        self.voltage_AC = voltage_ac
        self.current_discharge = current_discharge
        self.discharge = discharge
        self.capacity = capacity


# ======================================================================================================================


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


# ======================================================================================================================


class SolarModelMainMode:

    """SolarModelMainMode- класс предназначенный для определения поведения фотоэлектрических модулей с учетом внешних
    условий.
     Класс будет иметь связь между классами с нагрузкой, солнечным излучением, внешними факторами, инвертором,
     характеристиками солнечных панелей (отредачить!!!).
     Реализует расчет основного режима.
        Рассмотрим основной расчет.
        Описание методов и переменных:
            self.list_vah - объявляется списком, планируется содержать в себе расчетные ВАХ, выходной тип данных list,
            который содержит в себе тип collections.OrderedDict. (подобие словаря).
            self.solar_options - паспортные данные панелей.
            self.params - ???.
            def solar_radiation(self, sr, t) - Вычисляет значения пяти параметров для уравнения с одним диодом
            при эффективной освещенности и температуре ячейки с использованием модели CEC, sr - сол. радиация,
            t - температура.
            def pv(self) - вычисляет значения мощности, выходной тип pandas.core.frame.DataFrame.
            def mapping(data, key1, key2) - метод для получения отображения, data - данные для отображения,
            key1, key2 - ключи по которым отбираются данные.
    """

    def __init__(self):
        self.list_temp = []
        self.list_vah = []  # пустой лист для заполнения ВАХ
        self.solar_options = {'celltype': 'multiSi',  #
                              'STC': 224.99,
                              'PTC': 203.3,
                              'v_mp': 29.8,
                              'i_mp': 7.55,
                              'v_oc': 36.9,
                              'i_sc': 8.18,
                              'alpha_sc': 0.001636,
                              'beta_voc': -0.12177,
                              'gamma_pmp': -0.43,
                              'cells_in_series': 60,
                              'temp_ref': 25}

        self.params = pvlib.ivtools.sdm.fit_cec_sam(self.solar_options['celltype'],  # уточнить
                                                    self.solar_options['v_mp'], self.solar_options['i_mp'],
                                                    self.solar_options['v_oc'], self.solar_options['i_sc'],
                                                    self.solar_options['alpha_sc'],
                                                    self.solar_options['beta_voc'],
                                                    self.solar_options['gamma_pmp'],
                                                    self.solar_options['cells_in_series'],
                                                    self.solar_options['temp_ref'])

    def temperature_cell(self, s, temp):  # температура ячеек
        params = TEMPERATURE_MODEL_PARAMETERS["sapm"]["open_rack_glass_glass"]
        for i in range(24):
            t = round(float(temp[i]))
            sr = round(float(s[i]) * 1000)
            self.list_temp.append(sapm_cell(sr, t, 0, **params))
        return self.list_temp

    def solar_radiation(self, s, temp):

        for i in range(24):  # расчет ВАХ
            t = round(float(temp[i]))
            sr = round(float(s[i]) * 1000)
            if sr == 0:
                sr = 1
            options = pvlib.pvsystem.calcparams_cec(sr, t, self.solar_options['alpha_sc'], self.params[4],
                                                    self.params[0], self.params[1], self.params[3],
                                                    self.params[2], self.params[5])
            self.list_vah.append(pvlib.pvsystem.singlediode(options[0], options[1], options[2], options[3], options[4],
                                                            ivcurve_pnts=100, method="lambertw"))
        return self.list_vah

    def pv(self):  # получение расчет мощности
        list_p = []
        for vah in self.list_vah:
            list_i = []
            list_v = []
            for x in vah["i"]:
                list_i.append(x)
            for x in vah["v"]:
                list_v.append(x)
            list_p.append(pd.concat([pd.DataFrame([[list_i[i] * list_v[i], list_v[i]]], columns=["p", "v"])
                                     for i in range(len(list_i))], ignore_index=True))
        return list_p


# ======================================================================================================================


class Mapping:

    def __init__(self):
        pass

    @staticmethod
    def mapping_main(data, key1, key2):  # отображение графиков (по ключам)
        #  Для dOrderedDict
        if type(data) == list:
            for i in range(24):
                plt.plot(data[i][key1], data[i][key2])
                if key1 == "v" and key2 == "i":
                    plt.scatter(data[i]["v_mp"], data[i]["i_mp"])
        #  Для dataframe
        else:
            x = [int(data[key1][i]) for i in range(24)]
            y = [int(data[key2][i]) for i in range(24)]
            plt.plot(x, y)
        plt.show()

    @staticmethod
    def mapping_standby(spa_out):
        spa_out.plot()
        plt.show()


# ======================================================================================================================


class LogicEnablingMode:
    """
    Будет реализовывать логику режима (основной и резерв).
    class SolarModelStandbyMode - резервный
    class SolarModelMainMode - основной
    """
    pass


# ======================================================================================================================


def main():
    # ------------------------------------------------------------------------------------------------------------------
    # Резервный расчет
    latitude = 55.75
    longitude = 37.71
    loc = "Europe/Moscow"
    altitude = 186
    name = "Moscow"
    model_2 = SolarModelStandbyMode(latitude, longitude, loc, altitude, name)
    arr = [model_2.times, model_2.loc.latitude, model_2.loc.longitude]
    f = pvlib.solarposition.spa_python
    spa_out = model_2.solar_position(f, arr)
    apparent_zenith = spa_out["apparent_zenith"]
    model_map_2 = Mapping()
    model_map_2.mapping_standby(spa_out)
    arr = [model_2.times]
    f = pvlib.irradiance.get_extra_radiation
    spa_out = model_2.solar_position(f, arr)
    model_map_2.mapping_standby(spa_out)
    arr = [apparent_zenith]
    f = pvlib.clearsky.simplified_solis
    spa_out = model_2.solar_position(f, arr)
    model_map_2.mapping_standby(spa_out)

    # ------------------------------------------------------------------------------------------------------------------
    # Основной расчет
    data_solar = Data(";")
    data_meteo = Data(",")
    data_load = Data(";")
    data_solar.data = "SolarRadiation/USSR_full.csv"
    data_meteo.data = "DataMeteo/Tambient.csv"
    data_load.data = "Load/Load.csv"
    t = data_meteo.data[0]["Tambient"]
    sr = data_solar.data[0]["Global_irradiance"]
    model_1 = SolarModelMainMode()  # Параметры для панелей
    t = model_1.temperature_cell(sr, t)
    list_vah = model_1.solar_radiation(sr, t)
    list_p = model_1.pv()
    list_load = data_load.data[0]
    model_map_1 = Mapping()
    model_map_1.mapping_main(list_vah, key1="v", key2="i")
    model_map_1.mapping_main(list_p, key1="v", key2="p")
    model_map_1.mapping_main(list_load, key1="Hour", key2="Load")
    # ------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
