import datetime
import requests
import config

class Weather:

    def __init__(self):
        """
            Инициализация данных.

            __API_KEY - АПИ ключ к прогнозам.
            URL - Сервис погодных услуг
        """

        self.__API_KEY = config.API_KEY
        self.__URL = "http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/"

        self.params = {
            "apikey": self.__API_KEY,
            "language": "ru"
        }

        self.cities = {
            "Москва": ["294021", "bot/img/Moskwa.jpg"],
            "Ростов-на-Дону": ["295146", "bot/img/rostov-na-donu.jpg"],
            "Санкт-Петербург": ["295212", "bot/img/sant-petesburg.jpg"],
        }

    def get_all_cities(self):
        """
        Вовзращает список всех городов и их идентификаторы
        :return:
        """
        return self.cities

    def get_city(self, name_city: str):
        """
        Возвращает погодные данные указанного города
        :param name_city:
        :return:
        """
        if name_city in self.cities:
            parameters = {
                "apikey": self.__API_KEY,
                "language": "ru"
            }

            request: str = requests.get(self.__URL+self.cities[name_city][0], params=parameters).json()
            try:
                temp_c = round(self.convert_fr_to_cl(request[0]["Temperature"].get("Value")), 2)
                weather_state: str = request[0]["IconPhrase"]
                date_time: datetime = datetime.datetime.now()
                is_daylight: str = "День" if request[0]["IsDaylight"] else "Ночь"
            except KeyError:
                return None
            else:
                return temp_c, weather_state, date_time.strftime("%Y-%m-%d  %H-%M"), is_daylight
        else:
            return None

    def convert_fr_to_cl(self, fr: float):
        """
        Перевод с системы Фаренгейта в Цельсий
        :param fr:
        :return:
        """
        temperature_cl: float = (fr - 32) * (5/9)
        return temperature_cl
