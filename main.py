

# def main():
#     # ------------------------------------------------------------------------------------------------------------------
#     # Резервный расчет
#     latitude = 55.75
#     longitude = 37.71
#     loc = "Europe/Moscow"
#     altitude = 186
#     name = "Moscow"
#     model_2 = SolarModelStandbyMode(latitude, longitude, loc, altitude, name)
#     arr = [model_2.times, model_2.loc.latitude, model_2.loc.longitude]
#     f = pvlib.solarposition.spa_python
#     spa_out = model_2.solar_position(f, arr)
#     apparent_zenith = spa_out["apparent_zenith"]
#     model_map_2 = Mapping()
#     model_map_2.mapping_standby(spa_out)
#     arr = [model_2.times]
#     f = pvlib.irradiance.get_extra_radiation
#     spa_out = model_2.solar_position(f, arr)
#     model_map_2.mapping_standby(spa_out)
#     arr = [apparent_zenith]
#     f = pvlib.clearsky.simplified_solis
#     spa_out = model_2.solar_position(f, arr)
#     model_map_2.mapping_standby(spa_out)
#
#     # ------------------------------------------------------------------------------------------------------------------
#     # Основной расчет
#     data_solar = DataCSV(";")
#     data_meteo = DataCSV(",")
#     data_load = DataCSV(";")
#     data_solar.data = "SolarRadiation/USSR_full.csv"
#     data_meteo.data = "DataMeteo/Tambient.csv"
#     data_load.data = "DataLoad/DataLoad.csv"
#     t = data_meteo.data[0]["Tambient"]
#     sr = data_solar.data[0]["Global_irradiance"]
#     model_1 = SolarModelMainMode()  # Параметры для панелей
#     t = model_1.temperature_cell(sr, t)
#     list_vah = model_1.solar_radiation(sr, t)
#     list_p = model_1.pv()
#     list_load = data_load.data[0]
#     model_map_1 = Mapping()
#     model_map_1.mapping_main(list_vah, key1="v", key2="i")
#     model_map_1.mapping_main(list_p, key1="v", key2="p")
#     model_map_1.mapping_main(list_load, key1="Hour", key2="DataLoad")
#     # ------------------------------------------------------------------------------------------------------------------
#
#
# if __name__ == '__main__':
#     main()
