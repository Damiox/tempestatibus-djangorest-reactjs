import requests
import json
from functools import lru_cache


# WeatherService - current implementation is Wunderground API
# It will return an object of the required Weather data.
# Additionally, it adds a Cache (LRU) to avoid getting
# the Weather for the same Location several times.
class WeatherService:
    WUNDERGROUND_APIURL = 'http://api.wunderground.com'
    '/api/{}/almanac/conditions/q/{}/{}.json'
    WUNDERGROUND_APIKEY = 'bee225e8b1264f1c'

    class WeatherData:
        __weather = None
        __temp_curr = None
        __temp_high_avg = None
        __temp_low_avg = None
        __precipitating = None

        def __init__(self, weather, temp_curr,
                     temp_high_avg, temp_low_avg, precipitating):
            self.__weather = weather
            self.__temp_curr = temp_curr
            self.__temp_high_avg = temp_high_avg
            self.__temp_low_avg = temp_low_avg
            self.__precipitating = precipitating

        def __str__(self):
            return 'Weather is {}. Current Temp {}F,'
            ' Average=(High={}, Low={}), Precipitating={}'.format(
                self.get_weather(), self.get_temp_curr(),
                self.get_temp_high_avg(), self.get_temp_low_avg(),
                self.get_precipitating())

        def get_weather(self):
            return self.__weather

        def get_temp_curr(self):
            return self.__temp_curr

        def get_temp_high_avg(self):
            return self.__temp_high_avg

        def get_temp_low_avg(self):
            return self.__temp_low_avg

        def get_precipitating(self):
            return self.__precipitating

    def classify(self, city_name):
        forecast = self.getWeather(city_name)

        weather = forecast['current_observation']['weather']
        temp_curr = forecast['current_observation']['temp_f']
        temp_high = float(
            forecast['almanac']['temp_high']['normal']['F'])
        temp_low = float(
            forecast['almanac']['temp_low']['normal']['F'])
        precipitating = float(
            forecast['current_observation']['precip_today_metric'])
        return WeatherService.WeatherData(
            weather, temp_curr, temp_high, temp_low, precipitating)

    # This cache should also expiry elements after some time...
    @lru_cache(maxsize=100)
    def getWeather(self, city_name):
        location_data = city_name.split(', ')
        forecast_url = WeatherService.WUNDERGROUND_APIURL.format(
            WeatherService.WUNDERGROUND_APIKEY,
            location_data[1], location_data[0])
        response = requests.get(forecast_url)
        return json.loads(response.content.decode('utf-8'))
