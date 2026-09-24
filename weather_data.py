import time
import pandas as pd
import numpy as np
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class WeatherData():
	def __init__(self, lat, long):
		self.lat = lat
		self.long = long

		self.session = requests.Session()

		retry = Retry(
			total=3,
			connect=3,
			read=3,
			status=3,
			backoff_factor=1,
			status_forcelist=[429, 500, 502, 503, 504],
			allowed_methods=["POST"],
			raise_on_status=False,
		)

		adapter = HTTPAdapter(
			max_retries=retry,
			pool_connections=1,
			pool_maxsize=1,
		)

		self.session.mount("https://", adapter)
		self.session.mount("http://", adapter)

		self.url = "https://api.open-meteo.com/v1/forecast"
		self.attributes = {
			"latitude": self.lat,
			"longitude": self.long,
			"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_probability_max",
					  "wind_speed_10m_max"],
			"current": ["temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m",
						"wind_direction_10m", "precipitation_probability"],
			"timezone": "Europe/Berlin",
		}


	def retrieve_data(self):




		start = time.monotonic()

		try:
			response = self.session.get(
				self.url,
				params = self.attributes,
				timeout=(10, 30),
			)

			elapsed = time.monotonic() - start

			response.raise_for_status()
			data = response.json()
			self.data = data
			self.process_data()

			#print(
			#	f"OpenMeteo request successful: "
			#	f"time={elapsed:.2f}s"
			#)
			return True

		except requests.exceptions.Timeout:
			print(
				f"OpenMeteo request timed out: "
			)

		except requests.exceptions.ConnectionError as e:
			print(
				f"OpenMeteo connection error: "
				f"{e}"
			)

		except requests.exceptions.HTTPError as e:
			print(
				f"OpenMeteo HTTP error: "
				f"status={response.status_code}: {e}"
			)

		except ValueError as e:
			print(
				f"Open Meteo returned invalid JSON: "
				f"{e}"
			)

		except requests.exceptions.RequestException as e:
			print(
				f"Open Meteo request failed: "
				f"{e}"
			)

		except Exception as e:
			print(
				f"Unexpected error retrieving Open Meteo data: "
				f"{e}"
			)

		return False

	def process_data(self):
		data = self.data

		# Process current data
		current = data["current"]

		self.current_temperature_2m = current["temperature_2m"]
		self.current_relative_humidity_2m = current["relative_humidity_2m"]
		self.current_weather_code = str(int(current["weather_code"]))
		self.current_wind_speed_10m = current["wind_speed_10m"]
		self.current_wind_direction_10m = current["wind_direction_10m"]
		self.current_precipitation_propability = current["precipitation_probability"]

		# Process daily data
		daily = data["daily"]

		self.daily_weather_code = np.array(daily["weather_code"])
		self.daily_temperature_2m_max = np.array(daily["temperature_2m_max"])
		self.daily_temperature_2m_min = np.array(daily["temperature_2m_min"])
		self.daily_precipitation_probability_max = np.array(
			daily["precipitation_probability_max"]
		)
		self.daily_wind_speed_10m_max = np.array(
			daily["wind_speed_10m_max"]
		)

		# Create daily DataFrame
		daily_data = {
			"date": pd.to_datetime(daily["time"]),
			"weather_code": self.daily_weather_code,
			"temperature_2m_max": self.daily_temperature_2m_max,
			"temperature_2m_min": self.daily_temperature_2m_min,
			"precipitation_probability_max": (
				self.daily_precipitation_probability_max
			),
			"wind_speed_10m_max": self.daily_wind_speed_10m_max
		}

		self.daily_dataframe = pd.DataFrame(data=daily_data)

	def get_current_temperature(self) -> str:
		return str(round(self.current_temperature_2m)) + ' °C'

	def get_current_relative_humidity(self) -> str:
		return str(int(self.current_relative_humidity_2m)) + ' % rH'

	def get_current_weather_code(self) -> str:
		return str(self.current_weather_code)

	def get_current_wind_speed_10m(self) -> str:
		return str(int(self.current_wind_speed_10m)) + ' m/s'

	def get_current_wind_direction_10m(self) -> str:
		return str(self.current_wind_direction_10m)

	def get_current_precipitation_propability(self) -> str:
		return str(int(self.current_precipitation_propability)) + ' %'

	def get_current_min_max_temp(self) -> str:
		return str(round(self.daily_dataframe['temperature_2m_min'][0])) + ' °C / ' + str(round(self.daily_dataframe['temperature_2m_max'][0])) + ' °C'

	def get_forecast_weather_code(self, day : int) -> str:
		return str(int(self.daily_dataframe['weather_code'][day]))

	def get_forecast_min_max_temp(self, day : int) -> tuple():
		return (str(round(self.daily_dataframe['temperature_2m_min'][day])) + ' °C', str(round(self.daily_dataframe['temperature_2m_max'][day])) + ' °C')

	def get_forecast_wind_speed_10m(self, day : int) -> str:
		return str(int(self.daily_dataframe['wind_speed_10m_max'][day])) + ' m/s'

	def get_forecast_precipitation_propability(self, day : int) -> str:
		return str(int(self.daily_dataframe['precipitation_probability_max'][day])) + ' %'

if __name__ == "__main__":
	weather = WeatherData(51.0509,13.7383)
	weather.retrieve_data()

	print(weather.get_current_temperature())
	print(weather.get_current_relative_humidity())
	print(weather.get_current_weather_code())
	print(weather.get_current_wind_speed_10m())
	print(weather.get_current_wind_direction_10m())
	print(weather.get_forecast_precipitation_propability(0))

	for i in range(0,7):
		print(weather.get_forecast_min_max_temp(i))
		print(weather.get_forecast_weather_code(i))
		print(weather.get_forecast_wind_speed_10m(i))
		print(weather.get_forecast_precipitation_propability(i))
