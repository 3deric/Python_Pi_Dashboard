import matplotlib

import weather_data
import matplotlib.pyplot as plt
import numpy as np


def plot_weather_graph(weather : weather_data.WeatherData, size : tuple = (10,5)) -> plt.Figure:
	plt.style.use('_mpl-gallery')
	fig, ax1 = plt.subplots(figsize=size)

	ax1.plot(weather.get_forecast_hourly_temperature_2m()[0:25], linewidth=2, color='r', label='Temperature (°C)')
	ax1.set_xlabel('Hour')
	ax1.set_xticks(np.arange(0, 25, 2))
	ax1.set_ylabel('Temperature (°C)', color='r')
	# ax1.set_yticks(np.arange(-10,40,10))
	ax1.tick_params(axis='y', labelcolor='r')
	ax1.grid(False, "both", "y")

	ax2 = ax1.twinx()
	ax2.plot(weather.get_forecast_hourly_precipitation()[0:24], linewidth=2, label='Precipitation (mm)')
	ax2.set_ylabel('Precipitation (mm)', color='b')
	# ax2.set_yticks(np.arange(0,101,10))
	ax2.tick_params(axis='y', labelcolor='b')
	ax2.grid(False)

	# plt.title('Weather Forecast')
	fig.tight_layout()
	print(fig)
	return fig


if __name__ == "__main__":
	weather = weather_data.WeatherData(51.0509,13.7383)
	weather.retrieve_data()

	print(weather.get_forecast_hourly_temperature_2m())

	plot_weather_graph(weather)
	plt.show()


