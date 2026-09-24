from tkinter import font

import weather_data
import matplotlib.pyplot as plt
import numpy as np

LIGHT_COLOR = '#dbdbdb'

def plot_weather_graph(weather : weather_data.WeatherData, size : tuple = (7.5,5)) -> plt.Figure:
	plt.style.use('_mpl-gallery')
	plt.rcParams.update({'font.size': 14})
	fig, ax1 = plt.subplots(figsize=size)
	fig.patch.set_facecolor(LIGHT_COLOR)

	#ax1_plot = ax2.plot(weather.get_forecast_hourly_precipitation()[0:24], linewidth=2, label='Rain %')
	#ax1.set_xlabel('Time in hours')
	ax1_plot = ax1.bar(range(25),weather.get_forecast_hourly_precipitation()[0:25], color='#3b8ed0', label='Rain %')
	#ax1.set_ylabel('Rain propability in %', color='b')
	ax1.set_yticks(np.arange(0,101,25))
	ax1.tick_params(axis='y', labelcolor='#3b8ed0')
	ax1.grid(False)
	ax1.set_facecolor(LIGHT_COLOR)

	ax2 = ax1.twinx()
	ax2_plot = ax2.plot(weather.get_forecast_hourly_temperature_2m()[0:25], linewidth=4, color='#ca696e', label='Temp (°C)')
	ax2.set_xticks(np.arange(0, 25, 6))
	#ax2.set_ylabel('Temperature in °C', color='r')
	ax2.tick_params(axis='y', labelcolor='#ca696e')
	ax2.grid(False, "both", "y")
	ax2.set_facecolor(LIGHT_COLOR)

	fig.tight_layout()
	return fig


if __name__ == "__main__":
	weather = weather_data.WeatherData(51.0509,13.7383)
	weather.retrieve_data()

	print(weather.get_forecast_hourly_temperature_2m())

	plot_weather_graph(weather)
	plt.show()


