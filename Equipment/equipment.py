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
