import string

import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

class WeatherData():
	def __init__(self, lat, long):
		self.lat = lat
		self.long = long

		# Setup the Open-Meteo API client with cache and retry on error
		self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
		self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
		self.openmeteo = openmeteo_requests.Client(session=self.retry_session)

		# Make sure all required weather variables are listed here
		# The order of variables in hourly or daily is important to assign them correctly below
		self.url = "https://api.open-meteo.com/v1/forecast"
		self.params = {
			"latitude": self.lat,
			"longitude": self.long,
			"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_probability_max",
					  "wind_speed_10m_max"],
			"current": ["temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m",
						"wind_direction_10m", "precipitation"],
			"timezone": "Europe/Berlin",
		}
		
	def retrieve_data(self):
		responses = self.openmeteo.weather_api(self.url, params=self.params)
		# Process first location. Add a for-loop for multiple locations or weather models
		response = responses[0]
		print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
		print(f"Elevation: {response.Elevation()} m asl")
		print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
		print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

		# Process current data. The order of variables needs to be the same as requested.
		current = response.Current()
		self.current_temperature_2m = current.Variables(0).Value()
		self.current_relative_humidity_2m = current.Variables(1).Value()
		self.current_weather_code = current.Variables(2).Value()
		self.current_wind_speed_10m = current.Variables(3).Value()
		self.current_wind_direction_10m = current.Variables(4).Value()
		self.current_precipitation = current.Variables(5).Value()

		# Process daily data. The order of variables needs to be the same as requested.
		daily = response.Daily()
		daily_weather_code = daily.Variables(0).ValuesAsNumpy()
		daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
		daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
		daily_precipitation_probability_max = daily.Variables(3).ValuesAsNumpy()
		daily_wind_speed_10m_max = daily.Variables(4).ValuesAsNumpy()

		daily_data = {"date": pd.date_range(
			start = pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
			end =  pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = daily.Interval()),
			inclusive = "left"
		)}

		daily_data["weather_code"] = daily_weather_code
		daily_data["temperature_2m_max"] = daily_temperature_2m_max
		daily_data["temperature_2m_min"] = daily_temperature_2m_min
		daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
		daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max

		daily_dataframe = pd.DataFrame(data = daily_data)
		print(daily_dataframe)

	def get_current_temperature(self) -> string:
		return self.current_temperature_2m

	def get_current_relative_humidity(self) -> string:
		return self.current_relative_humidity_2m

	def get_current_weather_code(self) -> string:
		return self.current_weather_code

	def get_current_wind_speed_10m(self) -> string:
		return self.current_wind_speed_10m

	def get_current_wind_direction_10m(self) -> string:
		return self.current_wind_direction_10m

	def get_current_precipitation(self) -> string:
		return self.current_precipitation

if __name__ == "__main__":
	weather = WeatherData(51.0509,13.7383)
	weather.retrieve_data()

	print(f"Current temperature_2m: {weather.get_current_temperature()}")
	print(f"Current relative_humidity_2m: {weather.get_current_relative_humidity()}")
	print(f"Current weather_code: {weather.get_current_weather_code()}")
	print(f"Current wind_speed_10m: {weather.get_current_wind_speed_10m()}")
	print(f"Current wind_direction_10m: {weather.get_current_wind_direction_10m()}")
	print(f"Current precipitation: {weather.get_current_precipitation()}")

