import weather_data
import matplotlib.pyplot as plt



if __name__ == "__main__":
	weather = weather_data.WeatherData(51.0509,13.7383)
	weather.retrieve_data()

	print(weather.get_forecast_hourly_temperature_2m())

	plt.style.use('_mpl-gallery')
	fig,ax1 = plt.subplots()

	ax1.plot(weather.get_forecast_hourly_temperature_2m()[0:24],linewidth = 2, color = 'r', label='Temperature (°C)')
	ax1.set_xlabel('Hour')
	ax1.set_ylabel('Temperature (°C)', color = 'r')
	ax1.tick_params(axis='y', labelcolor='r')

	ax2 = ax1.twinx()
	ax2.plot(weather.get_forecast_hourly_precipitation()[0:24],linewidth = 2, label='Precipitation (mm)')
	ax2.set_ylabel('Precipitation (mm)', color = 'b')
	ax2.tick_params(axis='y', labelcolor='b')

	plt.title('Weather Forecast')
	fig.tight_layout()

	plt.show()

