import LogicMode.Mode.MainMode.mainMode as mainMode
import Mapping.mappingData as mp


class LogicEnablingMode:
    def __init__(self):
        self.flag = True
        self.solar_main = mainMode.SolarModelMainMode()
        self.map_data = mp.Mapping

    def logic(self):
        if self.flag:
            list_vah = self.solar_main.solar_radiation()
            print(list_vah)
            list_pv = self.solar_main.pv()
            self.map_data.mapping_main(list_vah, key1="v", key2="i")
            self.map_data.mapping_main(list_pv, key1="v", key2="p")


a = LogicEnablingMode()
a.logic()
