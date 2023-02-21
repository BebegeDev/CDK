import matplotlib.pyplot as plt


class Mapping:
    """ Mapping - класс для отображения графиков. Основного и резервного режима
    """

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
