from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps


class MyWeather():

    def __init__(self):
        owm = OWM('165069cfb23b96fccbe9a1b5841bc3e4')
        self.mgr = owm.weather_manager()

    def get_standardWeather(self, city, country):
        observation = self.mgr.weather_at_place(f'{city},{country}')
        w = observation.weather
        return f"In {city} it's {str(w.detailed_status)} and there is a temperature of {w.temperature('celsius')['temp']} degrees"

# w.detailed_status         # 'clouds'
# w.wind()                  # {'speed': 4.6, 'deg': 330}
# w.humidity                # 87
# w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
# w.rain                    # {}
# w.heat_index              # None
# w.clouds                  # 75
