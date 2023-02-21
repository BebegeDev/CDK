from LogicMode.Mode.MainMode.Data.DataOpenCSV import DataCSV
import pvlib

data_solar = DataCSV(";")
data_meteo = DataCSV(",")
data_load = DataCSV(";")
data_meteo.data = "/home/alexvb/PycharmProjects/CDK/Resources/DataMeteo/Tambient.csv"
data_solar.data = "/home/alexvb/PycharmProjects/CDK/Resources/DataSolar/USSR_full.csv"
data_load.data = "/home/alexvb/PycharmProjects/CDK/Resources/DataLoad/Load.csv"

solar_options = {'celltype': 'multiSi',
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

params = pvlib.ivtools.sdm.fit_cec_sam(solar_options['celltype'],  # уточнить
                                       solar_options['v_mp'], solar_options['i_mp'],
                                       solar_options['v_oc'], solar_options['i_sc'],
                                       solar_options['alpha_sc'],
                                       solar_options['beta_voc'],
                                       solar_options['gamma_pmp'],
                                       solar_options['cells_in_series'],
                                       solar_options['temp_ref'])

t = data_meteo.data[0]["Tambient"]
sr = data_solar.data[0]["Global_irradiance"]

