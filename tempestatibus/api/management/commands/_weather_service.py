import requests
import json
from functools import lru_cache

class WeatherService:
	WUNDERGROUND_APIURL = 'http://api.wunderground.com/api/{}/almanac/conditions/q/{}/{}.json';
	WUNDERGROUND_APIKEY = 'bee225e8b1264f1c';

	class WeatherData:
		__weather = None
		__temp_curr = None
		__temp_diff_avg = None

		def __init__(self, weather, temp_curr, temp_diff_avg):
			self.__weather = weather
			self.__temp_curr = temp_curr
			self.__temp_diff_avg = temp_diff_avg

		def get_weather(self):
			return self.__weather

		def get_temp_curr(self):
			return self.__temp_curr

		def get_temp_diff_avg(self):
			return self.__temp_diff_avg

	def classify(self, city_name):
		forecast = self.getWeather(city_name)
		weather = forecast['current_observation']['weather']
		temp_curr = forecast['current_observation']['temp_f']
		temp_high = int(forecast['almanac']['temp_high']['normal']['F'])
		temp_low = int(forecast['almanac']['temp_low']['normal']['F'])
		return WeatherService.WeatherData(weather, temp_curr, (temp_high - temp_low) / 2)

	@lru_cache(maxsize=100)
	def getWeather(self, city_name):
		location_data = city_name.split(', ')
		forecast_url = WeatherService.WUNDERGROUND_APIURL.format(WeatherService.WUNDERGROUND_APIKEY, location_data[1], location_data[0])
		# TODO: Error Handling
		response = requests.get(forecast_url)
		return json.loads(response.content.decode('utf-8'))
