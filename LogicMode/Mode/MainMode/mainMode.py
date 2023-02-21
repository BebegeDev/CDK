import pvlib
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS, sapm_cell
import Util.util as util
import pandas as pd


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
        self.t = util.t
        self.sr = util.sr
        self.solar_options = util.solar_options
        self.params = util.params
        self.list_temp = self.temperature_cell()
        self.list_vah = []

    def temperature_cell(self): # температура ячеек
        list_temp = []
        params = TEMPERATURE_MODEL_PARAMETERS["sapm"]["open_rack_glass_glass"]
        for i in range(24):
            temp = round(float(self.t[i]))
            solar_rad = round(float(self.sr[i]) * 1000)
            list_temp.append(sapm_cell(solar_rad, temp, 0, **params))
        return list_temp

    def solar_radiation(self):
        for i in range(24):  # расчет ВАХ
            temp = round(float(self.list_temp[i]))
            sr = round(float(self.sr[i]) * 1000)
            if sr == 0:
                sr = 1
            options = pvlib.pvsystem.calcparams_cec(sr, temp, self.solar_options['alpha_sc'], self.params[4],
                                                    self.params[0], self.params[1], self.params[3],
                                                    self.params[2], self.params[5])
            self.list_vah.append(pvlib.pvsystem.singlediode(options[0], options[1], options[2], options[3], options[4],
                                                            ivcurve_pnts=100, method="lambertw"))
        return self.list_vah

    def pv(self):  # получение расчет мощности
        list_p = []
        for vah in self.solar_radiation():
            list_i = []
            list_v = []
            for x in vah["i"]:
                list_i.append(x)
            for x in vah["v"]:
                list_v.append(x)
            list_p.append(pd.concat([pd.DataFrame([[list_i[i] * list_v[i], list_v[i]]], columns=["p", "v"])
                                     for i in range(len(list_i))], ignore_index=True))
        return list_p



